from apps.control.views.profiles import dashboard, user_list, user_edit
from apps.control.views.places import place_list, place_show, place_form, address_form, gallery_photo, change_image

from apps.control.views.events import event_list, event_form, event_show
from apps.control.views.spec import spec_list, spec_form, spec_show
from apps.control.views.sale import sale_list, sale_form, sale_show, sale_delete
from apps.control.views.tea import tea_list, tea_form, tea_show
from apps.control.views.news import news_list, news_form, news_show
from apps.control.views.photo import photoreport_list, photoreport_form, photoreport_photo_form, photoreport_show, photoreport_upload
from apps.control.views.actions import action_list, action_show, action_form, action_poll_form, workbidder_form, action_winner_form
from apps.control.views.seo import seo_form
from apps.control.views.grabers import *

__all__ = [dashboard, user_list, user_edit,
           place_list, place_show, place_form, address_form, gallery_photo,
           event_list, event_form, event_show,
           spec_list, spec_form, spec_show,
           sale_list, sale_form, sale_show, sale_delete,
           tea_list, tea_form, tea_show,
           news_list, news_form, news_show,
           photoreport_list, photoreport_form, photoreport_photo_form, photoreport_show, photoreport_upload,
           action_list, action_show, action_form, action_poll_form, workbidder_form, action_winner_form,
           seo_form,
           graber_dashboard, graber_clone_list, graber_place_update_list, graber_place_update_form
           ]
