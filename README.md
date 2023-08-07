# NORTON Inspiration App
An application created for NORTON Innovations's needs deals with printing projects using Stable Diffusion technology. The NORTON Inspiration app allows customers to create their picture of the wall and get creative and inspired by interacting with other registered users on the site. The user can add photos of his interior, where he wants to place graphics created for the client's needs by the company. Users inspire the post's author by commenting and uploading photos that are supposed to inspire the client to a project that becomes his dream.

![norton-inspiration-logo-white](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/d8e8e0a6-67ef-465d-b112-8ddf084c74d8)

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
The site assumes the registration and login of users. An unregistered user can view the posts page but cannot add a new post, like, or add comments. To enable this, the user must log in to the application. Then he gets the ability to add, edit and copy his posts and to like and add comments.

### Existing Features

 - **Navigation Bar**
    
    - The user has a marked logo and the option to go to the home page, register and log in. On the right side, there is a key message from NORTON Innovation - Where every wall tells a story. The registered user does not see the registration and login buttons and instead sees the logout and leaving the website button.
  
 ![Screenshot 2023-08-07 120209](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/3d142239-d96d-4f7f-99ce-1c69937f6f88)

  - **The Home Page**

    - The user on the main page sees all posts on the site, sorted from the most recent in the upper left corner. It can see the author of the post, photo, title, and subtitle of the post, along with the date of addition or update and the number of likes. There can be a maximum of 6 posts on the page; if there are more, the Add Post button will appear only after the user logs in.
   
![Screenshot 2023-08-07 120133](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/8e428171-e61c-4e25-9940-48afde738232)

  - **The Sign-Up Page**

    - The Sign Up page consists of the following fields: username, email, password, and re-entering the password. The user has a link to the login page if he is already registered.

![Screenshot 2023-08-07 120550](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/1752a74e-9257-4fde-a165-36fa0c265c40)

  - **The Login Page**

    - The login page consists of username, password, and option to remember me. If the user is not registered, there is a link to the registration page.
   
![Screenshot 2023-08-07 120933](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/89053592-74b2-427a-8a19-dd4061e2421b)

  - **The Add Post / Edit Post Page**

    - Add post / Edit post pages consisting of fields: title, subtitle, content, and a button for photo uploading. The maximum number of letters for the title field is 50 and for subtitles, 100. Images are automatically calibrated to smaller sizes to allow the customer to upload images of any size.
    - 
![Screenshot 2023-08-07 121234](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/5433da38-1e99-4521-92c8-56df3aa01aa2)

  - **The Delete Page**

    - The Delete page allows users to confirm whether they want to delete their post from the app.

![Screenshot 2023-08-07 121515](https://github.com/lukaszglowacz/norton-innovation-platform/assets/119242394/a55de6b6-6f3a-4f72-ac1a-f23305ed5e74)

- **The Post View Page**

    - The Post View page shows the photo the user uploaded to their post, the title, subtitle, and the date the post was uploaded or edited. Below is the post's content with the possibility of liking and seeing the total number of comments on the post. Below we see comments and the ability to write your comment. The comment requires the approval of the application admin.
 
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
 - Bootstrap: A popular front-end framework simplifies web design by providing pre-built responsive components and themes.
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

## Deployment

The site was deployed to Heroku.

The live link can be found here - https://norton-innovation-platform-edc4daea9f06.herokuapp.com/

The site was deployed to GitHub pages. The steps to deploy are as follows:

1. In the GitHub repository, navigate to the Settings tab.
2. Once in Settings, navigate to the Pages tab on the left-hand side.
3. Under Source, select the branch to master, then click Save.
4. Once the main branch has been selected, the page will be automatically refreshed with a detailed ribbon display to indicate the successful deployment.

The live link can be found here - https://github.com/lukaszglowacz/norton-innovation-platform

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
