![norton-inspiration-logo-white](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/d8e8e0a6-67ef-465d-b112-8ddf084c74d8)

An application created for NORTON Innovations's needs deals with printing projects using Stable Diffusion technology. The NORTON Inspiration app allows customers to create their picture of the wall and get creative and inspired by interacting with other registered users on the site. The user can add photos of his interior, where he wants to place graphics created for the client's needs by the company. Users inspire the post's author by commenting and uploading photos that are supposed to inspire the client to a project that becomes his dream.

## 🌐 Live View

You can access the live deployed version of the Norton Inspiration App here:

👉 **[Visit the Live App](https://norton-innovation-platform-89592d9b2194.herokuapp.com/)**  





## User Experience (UX)

### Design Choices
- Typography
  - The fonts chosen were 'Montserrat' for the headings and 'Catamaran' for the body text. They fall back to sans-serif, respectively.
  - 'Catamaran' is an easily readable font, and 'Montserrat' was selected via https://typ.io/search
  
- Colour Scheme
  - The leading color is #232129, which fits perfectly with the NORTON Innovation content.
  - The colors were selected via http://colormind.io/

![Screenshot 2023-08-07 115115](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/defff055-255c-4706-bc91-013d44aa2137)

## Features
The site assumes the registration and login of users. An unregistered user can view the posts page but cannot add a new post, like, or add comments. To enable this, the user must log in to the application. Then he can add, edit, and copy his posts and to like and add comments.

### Existing Features

 - **Navigation Bar**
    
    - The user has a marked logo and the option to go to the home page, testimonials, contact, register, and log in. On the right side is a key message from NORTON Innovation - Where every wall tells a story. The registered user does not see the registration and login buttons and instead sees the logout and leaving the website button.
  
 ![navigation_bar](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/493f68a6-eebc-4617-af6e-013df22e2a1b)

  - **The Home Page**

    - The user on the main page sees all posts on the site, sorted from the most recent in the upper left corner. It can see the post's author, photo, title, and subtitle, along with the date of addition or update and the number of likes. There can be a maximum of 6 posts on the page; if there are more, the Add Post button will appear only after the user logs in.
   
![Screenshot 2023-08-07 120133](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/8e428171-e61c-4e25-9940-48afde738232)

- **The Testimonials Page**

    The Testimonials Page shows user reviews of the Norton Inspiration platform. Testimonials Page is programmed in such a way that user reviews scroll automatically, and the user can also scroll manually.

![testimonials](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/2bc37c64-ff67-4ece-95aa-3dc192a1fe64)

- **The Contact Page**

    - The user can also send a contact form to the company with comments regarding the platform's operation. The contact form contains a name field, e-mail address, and message content. The user can reset and send the form by clicking the Submit button. In the checkboxes, the user sees suggestions on what to enter in the form.
 
![contact_form](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/bdc1c522-fba5-4e45-9a54-5b90951deea2)

  - **The Sign-Up Page**

    - The Sign Up page consists of the following fields: username, email, password, and re-entering the password. The user has a link to the login page if he is already registered.

![Screenshot 2023-08-07 120550](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/1752a74e-9257-4fde-a165-36fa0c265c40)

  - **The Login Page**

    - The login page consists of a username, password, and option to remember me. If the user is not registered, there is a link to the registration page.
   
![Screenshot 2023-08-07 120933](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/89053592-74b2-427a-8a19-dd4061e2421b)

  - **The Add Post / Edit Post Page**

    - Add post / Edit post pages consisting of fields: title, subtitle, content, and a button for photo uploading. The maximum number of letters for the title field is 50, and for subtitles, 100. Images are automatically calibrated to smaller sizes to allow the customer to upload images of any size.
    - 
![Screenshot 2023-08-07 121234](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/5433da38-1e99-4521-92c8-56df3aa01aa2)

  - **The Delete Page**

    - The Delete page allows users to confirm whether they want to delete their post from the app.

![Screenshot 2023-08-07 121515](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/a55de6b6-6f3a-4f72-ac1a-f23305ed5e74)

- **The Post View Page**

    - The Post View page shows the photo the user uploaded to their post, the title, subtitle, and the date the post was uploaded or edited. Below is the post's content with the possibility of liking and seeing the total number of comments on the post. Below, we see comments and the ability to write your comments. The comment requires the approval of the application admin.
 
![Screenshot 2023-08-07 121623](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/199fb24e-4ea8-4e8b-a8ec-15a09a6581dc)

  - **The Footer**
    
    - The Footer consists of social media that redirects customers to the appropriate applications: LinkedIn, Facebook, Instagram, and YouTube.

![Screenshot 2023-08-07 120417](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/749bd208-1118-49d0-8d7a-b9fa0a5d3f6d)

### Features Left to Implement
 
 - Later plans include extension by quick linking of other posts to social media
 - Connection of the application with the NORTON Innovation website

## Technology Used
 
 - Django: A high-level web framework that enables rapid development of web applications. It follows the DRY (Don't Repeat Yourself) principle and is built using Python.
 - Python: A versatile programming language known for its simplicity and readability, widely used in web development, data analysis, artificial intelligence, and more.
 - Bootstrap: A popular front-end framework that simplifies web design by providing pre-built responsive components and themes.
 - PostgreSQL: An open-source relational database management system known for its performance, reliability, and extensibility and often used in conjunction with web applications to store and manage data.
 - Cloudinary: A cloud-based service that offers solutions for image and video management, including upload, storage, optimization, and delivery across various devices.
 - GitHub: A platform for version control and collaboration platform, allowing multiple people to work on projects simultaneously. They are used to host and edit websites, manage code repositories, and facilitate collaborative coding.
 - Photoshop: Professionals use Adobe's image editing software for photo manipulation, design, and digital artwork creation.
 

## Testing

The tests were done in Python via TestCase. In total, the application passed 27 tests. The tests covered all the modules that appeared in the application.

### Responsiveness Test

The responsive design tests were carried out manually with Google Chrome DevTools.

|  | Mobile S - 320px | Mobile M - 375px | Mobile L - 425px | Tablet - 768px | Laptop - 1024px | Laptop L - 1440px | 4K - 2560px |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Render | passed | passed | passed | passed | passed | passed | passed |
| Images | passed | passed | passed | passed | passed | passed | passed |
| Links | passed | passed | passed | passed | passed | passed | passed |

All responsiveness tests were successful. The site is ready to work with devices of various widths. In addition, the site has been adapted to large screens above 1440px.

### Browser Compatibility

The website was tested on the following browsers with no visible issues for the user:
- Google Chrome
- Microsoft Edge
- Mozilla Firefox
 
Appearance, functionality, and responsiveness were consistent for various device sizes and browsers.

### Unfixed Bugs

There are no known unfixed bugs on this site.

## Deployment (Heroku)
Below is the complete process of deploying the application on Heroku — from forking the repository, to configuring mail, database, Cloudinary, and creating a superuser to add testimonials.

### Fork & Clone
1. Go to GitHub and click Fork to create your own copy of the repository.
2. (Optional) Clone the project locally or work in VSCode.

### Required Files for Heroku
Make sure your project includes the following:
- requirements.txt
- Procfile
- .python-version (e.g., 3.11)
- Correctly configured settings.py:
  - DEBUG = False
  - SECRET_KEY pulled from environment variables
  - DATABASES configured via dj_database_url
  - Cloudinary configured for static and media storage
  - ALLOWED_HOSTS containing your Heroku app domain

Example Procfile:

```bash
web: gunicorn inspiration.wsgi
```

### Create the Heroku App
1. Log in to https://dashboard.heroku.com
2. Click New → Create new app
3. Provide a name and choose the region (EU recommended)
4. Go to Deploy → select GitHub
5. Connect your repository
6. (Optional) Enable Automatic Deploys

### Add Heroku Postgres
1. Go to the Resources tab
2. In the Add-ons search field, type Heroku Postgres
3. Choose the free plan
4. After provisioning, Heroku will automatically add DATABASE_URL to Config Vars

### Configure Cloudinary
1. Log in at https://cloudinary.com
2. Go to Dashboard
3. Copy the environment variable:

```bash
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

4. Add it to Heroku Settings → Config Vars:

```bash
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

### Configure Mailtrap (SMTP Testing)
Mailtrap updated its UI — the old “Email Testing” section is now under Sandboxes.

1. Log in to https://mailtrap.io
2. In the left menu select Sandboxes
3. Create or open an Inbox
4. Open the Integration tab and choose SMTP
5. Copy the SMTP credentials:

- Host: sandbox.smtp.mailtrap.io
- Port: 2525
- Username
- Password

Add them to Heroku Config Vars:

```bash
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_HOST_USER=YOUR_MAILTRAP_USERNAME
EMAIL_HOST_PASSWORD=YOUR_MAILTRAP_PASSWORD
DEFAULT_FROM_EMAIL=noreply@example.com
```

### Add Remaining Environment Variables
In Heroku → Settings → Config Vars, set:

```bash
SECRET_KEY=your_django_secret_key
DEBUG=False
```

### Deploy the App
1. Go to the Deploy tab
2. Choose the branch (usually main)
3. Click Deploy Branch
4. Heroku builds the app and runs collectstatic

### Run Migrations
After the deployment completes:

1. Go to More → Run console
2. Execute:

```bash
python manage.py migrate
```

### Create a Superuser (Admin Login)

Using Run console again:

```bash
python manage.py createsuperuser
```

Enter:
- username
- email
- password

Then log in at:

```bash
https://YOUR-HEROKU-APP.herokuapp.com/admin/
```

### Add Testimonials via Admin

1. Log in to the admin panel
2. Open the Testimonials model
3. Click Add
4. Fill in the name, job title, and testimonial text
5. Save the entry

### Deployment Complete
Your application is now successfully deployed with:

- Heroku Postgres
- Cloudinary (static & media storage)
- Mailtrap SMTP email testing
- Admin panel with superuser
- Testimonials added through Django Admin


## Credits
  - Inspiration of I Think Therefore I Blog CODE Institute template

### Content
  - Google Fonts - used for fonts
  - Font Awesome - used for icons
  - Colormind - used to generate color pallet
  - typ.io - used to generate two compatible types of icons
  
### Media
  - Unsplash - used to download license-free images
  - Adobe Illustrator - used to prepare and edit images.
