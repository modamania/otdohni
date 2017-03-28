##########################
# Place queries
##########################
TAXI_QUERY = {
    'query': 'select jos_places_company.id from jos_places_company left join jos_services_zaveds on (jos_places_company.id=jos_services_zaveds.zaved_id) where service_id=4',
    'head': ['id'],
}

CATEGORY_QUERY = {
    'query': 'select id, teg_id, ordering, second_name, published from jos_places_tags',
    'head': ['id', 'main_tag_id', 'order', 'name', 'is_published']
}

RATE_CATEGORY_QUERY = {
    'query': 'select id, tag_id, company_id from jos_places_category',
    'head': ['id', 'category_id', 'place_id']
}

PLACE_QUERY = {
    'query': 'select id, title, description, url, urlhits, email, logotype, logotype_alt, picture, picture_alt, published, promo_published, promo_from_date, promo_till_date, hits, extension_id from jos_places_company left join jos_places_company_extensions on jos_places_company.id=jos_places_company_extensions.company_id',
    'head': ['id', 'name', 'description', 'url',
            'urlhits', 'email', 'logotype',
            'logotype_alt', 'photo',
            'photo_alt', 'is_published',
            'promo_is_up', 'date_promo_up',
            'date_promo_down', 'hits', 'status']
}

ADDRESS_QUERY = {
    'query': 'select id, company_id, mainoffice, address, geopoint, district_id, phone, email from jos_places_address',
    'head': ['id', 'place_id', 'is_main_office',
            'address', 'geopoint', 'district',
            'phone', 'email']
}

ADDRESS_WORK_TIME_QUERY = {
    'query': 'select id, address_id, mon, tue, wed, thu, fri, sat, sun, from_time, till_time, day_off from jos_places_work_time',
    'head': ['id', 'address_id', 'mon', 'tue', 'wed',
            'thu', 'fri', 'sat', 'sun', 'from_time',
            'till_time', 'day_off']
}

PLACE_PHOTOS_QUERY = {
    'query': 'select id, photos from jos_places_company where photos is not null and photos not like ""',
    'head': ['id', 'image']
}

TAGS_CATEGORY_QUERY = {
    'query_select': 'select teg_id, parent_id from jos_places_tags where parent_id not like 0',
    'query_insert': """insert into place_placecategory_tagging
                        (tag_id, placecategory_id)
                        values (%s, %s)""",
    'head': []
}

TAGS_PLACE_QUERY = {
    'query_select': 'select teg_id, zaved_id from jos_tegs_zaveds',
    'query_insert': """insert into place_place_tagging
                        (tag_id, place_id)
                        values (%s, %s)""",
    'head': []
}


##########################
# News queries
##########################
NEWS_QUERY = {
    'query': 'select id, title, title_alias, created, introtext, jos_content.fulltext, img, sectionid from jos_content where sectionid=1',
    'head': ['id', 'title', 'slug', 'pub_date', 'short_text', 'full_text', 'image'],
}

##########################
# Subscriber queries
##########################
SUBSCRIBER_QUERY = {
    'query': 'select subscriber_id, user_id, subscriber_name, subscriber_email, confirmed, subscribe_date, subscribe_date from jos_letterman_subscribers where confirmed=1',
    'head': ['id', 'user_id', 'name_field', 'email_field', 'subscribed', 'subscribe_date', 'create_date'],
    }


##########################
# Photoreport queries
##########################
PHOTO_QUERY = {
    'query': 'select id, catid, imgtitle, imgoriginalname from jos_datsogallery',
    'head': ['id', 'photoreport_id', 'title', 'image'],
}

PHOTOREPORT_QUERY = {
    'query': 'select cid, name, dt, description, published, alias from jos_datsogallery_catg',
    'head': ['id', 'title', 'date_event', 'description',
             'is_published', 'slug'],
}

TAGS_PHOTOREPORT_QUERY = {
    'query_select': 'select teg_id, cat_id from jos_tegs_datsogallery',
    'query_insert': """insert into photoreport_photoreport_tags
                        (tag_id, photoreport_id)
                        values (%s, %s)""",
    'head': []
}


#########################
# Event queries
#########################
EVENT_QUERY = {
	"query":"\
			SELECT id, title, cat, new_picture, description, intro, video, picture, date_created, published, approved\
			FROM jos_afisha_eventdata\
            WHERE cat IN (14, 23, 26, 24, 25, 27)\
			",
	"head": ('id', 'title', 'category_id', 'image', 'description', 'intro', 'trailer', 'add_picture', 'pub_date', 'is_published', 'approved'),
	"votes_sql": "SELECT COUNT(*) FROM jos_afisha_events_votes WHERE id_event=%s",
	"star_sql": "SELECT AVG(star) from jos_afisha_events_votes WHERE id=%s",
	}

OCCURRENCE_QUERY = {
	"query":"\
			SELECT event.extid, event.group, zaved, start_date, end_date, extra_time, recur_count, recur_type, recur_val, recur_until, monday, tuesday, wednesday, thursday, friday, saturday, sunday\
			FROM jos_afisha_events AS event\
            INNER JOIN jos_places_company AS place\
            ON place.id = event.zaved\
			WHERE event.group=%s",
	"head": ('id', 'event_id', 'place_id', 'start_date', 'end_date', 'start_times', 'repeat_number', 'repeat_on', 'repeat_every', 'repeat_until', 'monday', 'thuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'),
	}

CATEGORU_QUERY = {
	"query":"\
            SELECT id , title FROM jos_categories\
            WHERE id IN (14, 23, 26, 24, 25, 27)",
	"head": ('id', 'title')
	}


########################
# Action queries
########################
ACTION_QUERY  = {
    'query': 'select id, title, title_alias, created, introtext, jos_content.fulltext, img, sectionid from jos_content where catid=86',
    'head': ('id', 'title', 'slug', 'pub_date', 'short_text', 'full_text', 'image'),
}

POLL_QUERY = {
    'query': 'select id, title, aktual from jos_spolls',
    'head': ('id', 'title', 'status'),
}

WORKBIDDER_QUERY = {
    'query': 'select id, poll_id, title, text from jos_spoll_responds',
    'head': ('id', 'poll_id', 'title', 'text'),
}
LIKE_QUERY = {
    'query_select': 'select respont_id, user_id from jos_spoll_votes where respont_id is not NULL',
    'query_insert': """insert into action_workbiddervote
                        (workbidder_id, user_id)
                        values (%s, %s)""",
    'head': []
}


##########################
# Comment queries
##########################
COMMENT_QUERY = {
    'query': 'select contentid, ip, name, comment, date, published, url from jos_akocomment',
    'head': ['object_pk', 'ip_address', 'user_name',
            'comment', 'submit_date']
}

PHOTO_COMMENT_QUERY = {
    'query': 'select cmtpic, cmtip, cmtname, cmttext, cmtdate from jos_datsogallery_comments where published=1',
    'head': ['object_pk', 'ip_address',
             'user_name', 'comment', 'submit_date']
}


##########################
# Tagging queries
##########################
TAG_QUERY = {
    'query': 'select id, name, alias from jos_tegs',
    'head': ['id', 'name', 'slug']
}


##########################
# Votes queries
#########################
VOTE_PLACE_QUERY = {
    'query': 'select id, votes, votesum from jos_places_company where votes>0',
    'head': ['object_id', 'votes', 'votesum']
}

VOTE_PHOTOREPORT_QUERY = {
    'query': 'select id, imgvotes, imgvotesum from jos_datsogallery where imgvotes>0',
    'head': ['object_id', 'votes', 'votesum']
}

VOTE_EVENT_QUERY = {
    'query': 'select id_event, id_user, star from jos_afisha_events_votes',
    'head': ['object_id', 'user_id', 'vote']
}

##########################
# Tea queries
#########################
TEA_QUERY = {
    "query": "select id, tea.title, img, tea.introtext, tea.created, tea.modified_by from jos_content as tea where title_alias like %s",
    "head": ['id', 'title', 'image', 'full_text', 'pub_date', 'is_published'],
}
