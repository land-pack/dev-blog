from app import db, models


# add base contact information
phone = "17666116392"
email = "landpack@sina.com"
leisure = "Mon - Fri 09:00 - 18:00"
content = """<p>I am in the website field since 2004 Lorem ipsum dolor 
            sit amet, consectetur adipiscing elit. Proin at quam at orci 
            commodo hendrerit vitae nec eros. Vestibulum neque est, imperdiet 
            nec tortor nec, tempor semper metus. <b>I am a developer</b>, et 
            accumsan nisi. Duis laoreet pretium ultricies. Curabitur rhoncus 
            auctor nunc congue sodales. Sed posuere nisi ipsum, eget dignissim 
            nunc dapibus eget. Aenean elementum sollicitudin sapien ut sapien 
            fermentum aliquet mollis. Curabitur ac quam orci sodales quam ut tempor.</p>
        """
title = """<h1>I am Looking for a <span class="main-color">
online presence</span>?</h1>"""

contact_addr = models.ContactInfo(
    phone=phone,
    email=email,
    leisure=leisure,
    content=content,
    title=title
)
db.session.add(contact_addr)


# add conect subject to database ~~
subjects = [
    "Website Design & Development",
    "Python Web",
    "Spider with Scrapy",
    "I Want to General Talk",
    "Other"

]

for subject in subjects:
    s = models.ContectSubjects(subject=subject)
    db.session.add(s)

# add recommend person data

recommend_list = [
    {
        "desc": """
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                Proin at quam at orci commodo hendrerit vitae nec eros. 
                Vestibulum neque est, imperdiet nec tortor nec, tempor semper metus.
            """,
        "com": "Rolling LTD, Founder",
        "name": "Jhon Doe"
    },
        {
        "desc": """
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                Proin at quam at orci commodo hendrerit vitae nec eros. 
                Vestibulum neque est, imperdiet nec tortor nec, tempor semper metus.
            """,
        "com": "WebRes LTD, Founder",
        "name": "Jhon Doe"
    }
]

for rec in recommend_list:
    r = models.RecommendInfo(name=rec['name'], com=rec['com'], desc=rec['desc'])
    db.session.add(r)

# add about data
greeting = 'Hey, I am ~'
username = 'Frank AK'
describer = 'something ~'
services = 'I can drink ~ | I can eating ~'
jobs = 'Python Developer'

ab = models.AboutInfo(
    username = username,
    greeting = greeting,
    describer = describer,
    services = services,
    jobs = jobs
    )
db.session.add(ab)

db.session.commit()
