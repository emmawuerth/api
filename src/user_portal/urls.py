from django.urls import path

from . import views

urlpatterns = [
  path('', views.home),
  path('actions',views.actions),
  path('menu', views.menu),
  path('aboutus', views.aboutUs),
  path('events', views.events),
  path('stories', views.stories),
  path('get/page',views.get_page),
  path('get/todo_actions', views.get_user_todo_actions),
  path('get/completed_actions', views.get_user_completed_actions),
  path('get/events', views.get_all_community_events),
  path('get/events/all', views.get_all_community_events),
  path('get/event', views.get_one_event),
  path('get/community_actions', views.get_community_actions),
  path('get/community_actions/all', views.get_community_actions),
  path('get/action', views.get_one_action),
  path('get/profile', views.get_my_profile),
  path('get/households', views.get_user_households),
  path('get/household', views.get_one_household),
  path('get/teams/all', views.get_community_teams),
  path('get/team', views.get_one_team),
  path('get/communities', views.get_all_communities),
  path('get/community', views.get_one_community),
  path('get/graph', views.get_one_community_graph),
  path('get/graphs', views.get_community_graphs),
  path('get/graphs/all', views.get_community_graphs),
  path('create/account', views.create_new_user),
  path('create/user', views.create_new_user),
  path('create/goal', views.create_goal),
  path('create/household', views.create_household),
  path('create/real_estate_unit', views.create_household),
  path('create/team', views.create_team),
  path('create/event', views.create_event),
  path('add/team_members', views.add_team_members),
  path('add/user_action', views.create_user_action),
  path('subscribe', views.create_subscriber),
  path('add/subscriber', views.create_subscriber),
  path('add/testimonial', views.add_testimonial),
  path('register_for_event', views.register_user_for_event),
  path('update/user_action', views.update_user_action),
  path('update/profile', views.update_profile),
  path('delete/user_action', views.delete_user_action),
  path('delete/user', views.delete_user_account)
]