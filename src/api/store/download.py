from _main_.utils.massenergize_errors import MassEnergizeAPIError, InvalidResourceError, ServerError, CustomMassenergizeError
from _main_.utils.massenergize_response import MassenergizeResponse
from _main_.utils.context import Context
from database.models import UserProfile, CommunityMember, Action, Team, UserActionRel, Testimonial, TeamMember
from django.db.models import Q, prefetch_related_objects
import traceback
import time

# TODO: proper logging/error handling to match Sam's work

class DownloadStore:

  def __init__(self):
    self.name = "Download Store/DB"


  def _all_users_download(self):
    pass


  def _community_users_download(self, community_id):
    # TODO: figure out which of these two queries I should use...
    # if the first one, make sure to select_related for the user
    users = [cm.user for cm in CommunityMember.objects.filter(community__id=community_id, is_deleted=False, user__is_deleted=False)]
    # print(users)
    users = UserProfile.objects.filter(communities__in=[community_id]).distinct()
    # print(users)

    # TODO: update actions query based on what works for the community actions query
    actions = Action.objects.filter(Q(community__id=community_id) | Q(is_global=True)) \
                                                      .filter(is_deleted=False)
    teams = Team.objects.filter(community__id=community_id, is_deleted=False)

    columns = ['full_name',
                'email',
                'role'] \
                + [action.title for action in actions] \
                + [team.name for team in teams]

    data = [columns]

    for user in users:

      row = [user.full_name,
            user.email,
            'super admin' if user.is_super_admin else
                'community admin' if user.is_community_admin else
                'vendor' if user.is_vendor else
                'community member']

      # create collections with constant-time lookup. VERY much worth the up-front compute.
      user_testimonial_action_ids = set([testimonial.action.id if testimonial.action else None
                                  for testimonial in Testimonial.objects.filter(user=user)])
      action_id_to_action_rel = {user_action_rel.action.id: user_action_rel
                                  for user_action_rel in UserActionRel.objects.filter(user=user)}

      for action in actions:
        user_action_status = ''
        if action.id in user_testimonial_action_ids:
          user_action_status = 'testimonial'
          end_time_1 = time.perf_counter()
        else:
          user_action_rel = action_id_to_action_rel.get(action.id, None)
          if user_action_rel:
            user_action_status = user_action_rel.status
          end_time_1 = time.perf_counter()
        row.append(user_action_status)

      user_team_members = TeamMember.objects.filter(user=user).select_related('team')

      for team in teams:
        user_team_status = ''
        team_member = user_team_members.filter(team=team).first()
        if team_member:
          if team_member.is_admin:
            user_team_status = 'admin'
          else:
            user_team_status = 'member'
        row.append(user_team_status)

      data.append(row)

    return data


  def _all_actions_download(self):
    pass


  def _community_actions_download(self, community_id):

    # TODO: this is listing MORE actions than are showing up on the portal
    # from list_for_community_admin and then filtering on front-end
    # for Kaat's test community, 15 show up on portal, 28 from this query
    # but it's the same query!!?!?!!?
    actions = Action.objects.filter(Q(community__id=community_id) | Q(is_global=True)) \
      .filter(is_deleted=False).select_related('calculator_action').prefetch_related('tags')

    columns = ['title',
              'average_carbon_points',
              'category',
              'cost',
              'impact']
    
    data = [columns]

    for action in actions:

      average_carbon_points = action.calculator_action.average_points \
                          if action.calculator_action else action.average_carbon_score
      category = action.tags.filter(tag_collection__name='Category').first()
      cost = action.tags.filter(tag_collection__name='Cost').first()
      impact = action.tags.filter(tag_collection__name='Impact').first()

      data.append([action.title,
                  average_carbon_points,
                  category.name if category else '',
                  cost.name if cost else '',
                  impact.name if impact else ''])

    return data


  def users_download(self, context: Context, community_id) -> (list, MassEnergizeAPIError):
    try:
      if context.user_is_super_admin:
        if community_id:
          return self._community_users_download(community_id), None
        else:
          return self._all_users_download(), None
      elif context.user_is_community_admin and community_id:
        return self._community_users_download(community_id), None
      else:
        # TODO: return error
        pass
    except Exception as e:
      print(traceback.format_exc())
      return None, CustomMassenergizeError(e)


  def actions_download(self, context: Context, community_id) -> (list, MassEnergizeAPIError):
    try:
      if context.user_is_super_admin:
          if community_id:
            return self._community_actions_download(community_id), None
          else:
            return self._all_actions_download(), None
      elif context.user_is_community_admin and community_id:
          return self._community_actions_download(community_id), None
      else:
          # TODO: return error
          pass
    except Exception as e:
      print(traceback.format_exc())
      return None, CustomMassenergizeError(e)
