from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView, TemplateView, UpdateView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model

from authentication.utilities import AccessRequiredMixin, require_access
from control_panel import forms



class StaffView(AccessRequiredMixin, TemplateView):
	template_name = 'control/users/staff.html'

	def get_context_data(self, *args, **kwargs):
		'''
		Render staff users and assign profile form to each user
		'''

		context = super().get_context_data(*args, **kwargs)
		# Initialize users that hare neither staff nor superuser
		users = (
			get_user_model().objects
			.exclude(Q(is_staff=False) | Q(is_superuser=False))
		)

		# To each user object attach an admin profile permissions form
		for i in users:
			i.form = forms.AdminProfileForm(instance=i, auto_id=False)

		context['users'] = users
		context['creation_form'] = forms.UserCreationForm()
		return context


	def post(self, request):
		'''
		Dispatcher for different types of forms
		'''

		form_type = request.POST.get('submit')
		if form_type == 'Update':
			return self.process_update(request)
		elif form_type == 'Create':
			return self.process_create(request)
		else:
			return HttpResponse(status=500)


	def process_update(self, request):
		'''
		Process form that updates admin profile permissions
		'''

		User = get_user_model()
		try:
			user = User.objects.get(pk=request.POST.get('pk'))
		except User.DoesNotExist:
			return HttpResponse(status=500)

		form = forms.AdminProfileForm(request.POST, instance=user)
		if form.is_valid():
			form.save()
		else:
			# Form doesn't have any permissions selected. Reset all.
			user.adminprofile.available_pages.set([])

		context = self.get_context_data()
		return render(request, self.template_name, context=context)


	def process_create(self, request):
		'''
		Process form that creates new user
		'''

		user_form = forms.UserCreationForm(request.POST)
		if user_form.is_valid():
			# Set is_staff to true before saving
			user_form.instance.is_staff = True
			user_form.save()
		else:
			user_form.expanded = 'true'

		context = self.get_context_data()
		context['creation_form'] = user_form
		return render(request, self.template_name, context=context)



class UserListView(AccessRequiredMixin, ListView):
	template_name = 'control/users/user-list.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['creation_form'] = forms.UserCreationForm()
		return context


	def post(self, request):
		self.object_list = self.get_queryset()
		user_form = forms.UserCreationForm(request.POST)
		context = self.get_context_data()

		if user_form.is_valid():
			user_form.save()
		else:
			user_form.expanded = 'true'
			context['creation_form'] = user_form

		return render(request, self.template_name, context=context)


	def get_queryset(self):
		q = (
			get_user_model().objects
			.exclude(Q(is_affiliate=True) | Q(is_staff=True) | Q(is_superuser=True))
			.prefetch_related(
				'payment_set',
				'payment_set__pendingitem_set'
			)
		)
		return q



class UserDetailView(AccessRequiredMixin, UpdateView):
	template_name = 'control/users/user-detail.html'
	fields = '__all__'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		return context

	def get_queryset(self):
		queryset = get_user_model().objects.all()
		return queryset



@require_http_methods(["POST"])
@require_access
def delete_user(request):
	pk = request.POST.get('pk')
	try:
		user = get_user_model().objects.get(pk=pk)
		user.delete()
		return HttpResponse('OK')
	except get_user_model().DoesNotExist:
		return HttpResponse('User does not exist', status=404)



@require_http_methods(["POST"])
@require_access
def toggle_user_permissions(request):
	uid = request.POST.get('user')
	try:
		user = get_user_model().objects.get(pk=int(uid))
	except (get_user_model().DoesNotExist, ValueError):
		return HttpResponse('User doesn\'t exitst / invalid id', status=406)

	permission = request.POST.get('permission')
	if permission == 'staff':
		new_status = not user.is_staff
		user.is_staff = new_status
	elif permission == 'active':
		new_status = not user.is_active
		user.is_active = new_status
	elif permission == 'superuser':
		new_status = not user.is_superuser
		user.is_superuser = new_status
	else:
		return HttpResponse('Wrong permission', status=406)

	user.save()
	return JsonResponse({'new_status': new_status})
