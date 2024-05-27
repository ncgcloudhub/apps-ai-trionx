import os

# Define the template
template = """{% extends "socialai/base.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <h1 class="mt-5 text-center">{{ header }}</h1>
    <form method="post" class="d-flex flex-column align-items-center">
        {% csrf_token %}
        <div class="mb-3 w-50">
            <label for="prompt" class="form-label">Enter your prompt:</label>
            <input type="text" id="prompt" name="prompt" class="form-control" required>
        </div>
        <div class="mb-3 w-50">
            <label for="content_type" class="form-label">Select content type:</label>
            <select id="content_type" name="content_type" class="form-select" required>
                <option value="{{ content_type }}">{{ content_type }}</option>
                <!-- Add more options as needed -->
            </select>
        </div>
        <button type="submit" class="btn btn-primary">Generate</button>
    </form>
{% endblock %}
"""

# Define the pages to be generated
pages = [
    {"filename": "youtube_title_generator.html", "title": "YouTube Title Generator", "header": "YouTube Title Generator", "content_type": "YouTube title"},
    {"filename": "youtube_tags_generator.html", "title": "YouTube SEO Tags Generator", "header": "YouTube SEO Tags Generator", "content_type": "YouTube tags"},
    {"filename": "youtube_description_generator.html", "title": "YouTube SEO Description Generator", "header": "YouTube SEO Description Generator", "content_type": "YouTube description"},
    {"filename": "tiktok_title_generator.html", "title": "TickTock Title Generator", "header": "TickTock Title Generator", "content_type": "TickTock title"},
    {"filename": "tiktok_tags_generator.html", "title": "TickTock SEO Tags Generator", "header": "TickTock SEO Tags Generator", "content_type": "TickTock tags"},
    {"filename": "tiktok_description_generator.html", "title": "TickTock SEO Description Generator", "header": "TickTock SEO Description Generator", "content_type": "TickTock description"},
    {"filename": "facebook_title_generator.html", "title": "Facebook Title Generator", "header": "Facebook Title Generator", "content_type": "Facebook title"},
    {"filename": "facebook_tags_generator.html", "title": "Facebook SEO Tags Generator", "header": "Facebook SEO Tags Generator", "content_type": "Facebook tags"},
    {"filename": "facebook_description_generator.html", "title": "Facebook SEO Description Generator", "header": "Facebook SEO Description Generator", "content_type": "Facebook description"},
    {"filename": "instagram_title_generator.html", "title": "Instagram Title Generator", "header": "Instagram Title Generator", "content_type": "Instagram title"},
    {"filename": "instagram_tags_generator.html", "title": "Instagram SEO Tags Generator", "header": "Instagram SEO Tags Generator", "content_type": "Instagram tags"},
    {"filename": "instagram_description_generator.html", "title": "Instagram SEO Description Generator", "header": "Instagram SEO Description Generator", "content_type": "Instagram description"},
    {"filename": "blog_title_generator.html", "title": "Blog Title Generator", "header": "Blog Title Generator", "content_type": "Blog title"},
    {"filename": "blog_introduction_generator.html", "title": "Blog Introduction Generator", "header": "Blog Introduction", "content_type": "Blog introduction"},
    {"filename": "blog_conclusion_generator.html", "title": "Blog Conclusion Generator", "header": "Blog Conclusion", "content_type": "Blog conclusion"},
    {"filename": "blog_body_generator.html", "title": "Blog Body Generator", "header": "Blog Description / Body", "content_type": "Blog body"},
    {"filename": "blog_tags_generator.html", "title": "Blog SEO Tags Generator", "header": "Blog SEO Tags Generator", "content_type": "Blog tags"},
    {"filename": "vlog_title_generator.html", "title": "Vlog Title Generator", "header": "Vlog Title Generator", "content_type": "Vlog title"},
    {"filename": "vlog_tags_generator.html", "title": "Vlog SEO Tags Generator", "header": "Vlog SEO Tags Generator", "content_type": "Vlog tags"},
    {"filename": "vlog_description_generator.html", "title": "Vlog SEO Description Generator", "header": "Vlog SEO Description Generator", "content_type": "Vlog description"},
]

# Generate the HTML files
output_dir = "socialai/templates/socialai"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for page in pages:
    content = template.replace("{{ title }}", page["title"]).replace("{{ header }}", page["header"]).replace("{{ content_type }}", page["content_type"])
    with open(os.path.join(output_dir, page["filename"]), "w") as f:
        f.write(content)

print("HTML files have been generated, located at: " + output_dir)
