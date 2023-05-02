from django.shortcuts import render, redirect
from .forms import NewUserForm, ResumeForm, EditUserForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Job, Resume
from django.contrib.auth.forms import AuthenticationForm
import PyPDF2
from .recommender import recommend


def homepage(request):
	if request.user.is_authenticated==False:
		return redirect("login")
	return render(request, 'main/homepage.html')

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="user/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="user/login.html", context={"login_form":form})

def edit_request(request):
	if request.user.is_authenticated==False:
		return redirect("login")
	else: 
		if request.method == "POST":
			form = EditUserForm(request.POST, instance=request.user)
			if form.is_valid():
				form.save()
				return redirect("edit")
		form = EditUserForm()

	return render(request, 'main/edit.html', {'form_edit': form})

def upload_pdf(request):
	if request.user.is_authenticated==False:
		return redirect("login")
	else:
		if request.method == 'POST':
			form = ResumeForm(request.POST, request.FILES)
			if form.is_valid():
				newdoc = Resume(pdf_file=request.FILES['pdf_file'], user=request.user)
				newdoc.save()

				# Extract text from pdf
				pdf_file = PyPDF2.PdfReader(newdoc.pdf_file)
				text = ""
				for page in range(len(pdf_file.pages)):
					text += pdf_file.pages[page].extract_text()

				# Process the text

				# Save processed text to model
				newdoc.text_content = text
				newdoc.save()

				# Save processed text in session
				request.session['text'] = text

				return redirect("results")  # redirect to a new view to show the results
		else:
			form = ResumeForm()

		return render(request, 'showjob/upload.html', {'form': form})

def resumes(request):
	if request.user.is_authenticated==False:
		return redirect("login")
	else:
		resumes = Resume.objects.filter(user=request.user)
		return render(request, 'showjob/resumes.html', {'resumes': resumes})
	
def resume_detail(request, id):
	if request.user.is_authenticated==False:
		return redirect("login")
	else:
		data = Resume.objects.get(pk=id)
		if request.method == 'GET':
			form = ResumeForm(request.GET, instance=data)
			if form.is_valid():
				text = data.text_content
				request.session['text'] = text

				return redirect("results")
			else:
				form = ResumeForm()
		return render(request, 'showjob/resume_detail.html', {'resume': data})

def show_results(request):
	if request.user.is_authenticated==False:
		return redirect("login")
	else:
		jobs = Job.objects.all()
		jobs_arr = []
		for i in jobs:
			jobs_arr.append({
				'id': i.id,
				'title': i.title,
				'company': i.company,
				'url': i.url,
				'description': i.description
			})
		text = request.session.get('text')
		if text==None:
			return redirect("resultserror")
		else:
			recomms = recommend(text,jobs_arr)
			jobs = Job.objects.filter(id__in=recomms)
			jobs_dict = dict([(job.id, job) for job in jobs])
			sorted_jobs = [jobs_dict[id] for id in recomms]
		return render(request, 'showjob/results.html', {'jobs': sorted_jobs})

def results_error(request):
	return render(request, 'showjob/resultserror.html')