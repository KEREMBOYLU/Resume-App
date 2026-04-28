# CMS Keys

Use this file while filling the Django admin CMS.

General rule:

```text
short text / title / label / URL / email / placeholder -> parameter
long description / paragraph / subtitle / message -> text_parameter
images -> ImageSetting.file
```

## Site General

```text
site_title = parameter
site_keywords = parameter
site_description = text_parameter
site_author = parameter
site_brand_short = parameter
site_nav_cv_label = parameter
site_footer_brand = parameter
site_footer_copyright = parameter
```

## Home Hero

```text
home_hero_profile_alt = parameter
home_hero_greeting = parameter
home_hero_role = parameter
home_hero_passion = parameter
home_hero_location = parameter
home_hero_contact_email = parameter
```

## Home About

```text
home_about_subtitle = text_parameter
home_about_paragraph_1 = text_parameter
home_about_paragraph_2 = text_parameter
```

## Contact Page

```text
contact_page_title = parameter
contact_success_message = text_parameter
contact_error_message = text_parameter

contact_info_address_desc = text_parameter
contact_info_phone_desc = parameter
contact_info_email_desc = parameter

contact_form_name_placeholder = parameter
contact_form_email_placeholder = parameter
contact_form_subject_placeholder = parameter
contact_form_message_placeholder = parameter
```

## Image Settings

These are not `GeneralSetting` records. Add them in `ImageSetting`.

```text
favicon = file
home_hero_profile_image = file
```

## Not Active

Keys like `project_apex_*`, `project_lumina_*`, and `projects_card_*` are legacy seed keys and are not used by the current active project pages.

Projects are filled through these admin models:

```text
Project
ProjectCategory
ProjectImage
ProjectLink
ProjectSection
```
