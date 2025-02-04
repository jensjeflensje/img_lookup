# Image Lookup
A web tool to inspect images.
It has metadata lookups, location data lookups, image hashes,
OCR text recognition, landmark recognition, and web search.

I host the site on https://butwhe.re,
on which everyone can access it.

## About the application
When you drag a file onto the initial dropzone on the site,
it'll upload the file to S3.
After it's uploaded, it'll "finalize" the upload with the backend.
Once the backend has validated the upload, it'll start the "inspections".
An inspection is a type of lookup on the image.
Each inspection has its own widget which displays the inspection's output.
An inspection can take a while (usually between 1 and 5 seconds),
so the frontend polls the backend every 500ms to see if it's done.
When it's done, it'll display it on the site.

## Asset lifetime
By default, an asset will be in the system for 2 hours,
after which, it'll be deleted completely (alongside the inspection data).
If you extend the lifetime of an asset, it'll be saved for 7 days.
The extend feature makes it possible to share the link with others.

## Frontend
The frontend is made with VueJS in TypeScript.
I'm using PrimeVue as a base for my dialogs, tables etc.

## Backend
I'm using Django as a backend with Django Rest Framework.
I'm using Django Q as a task queue to execute inspections.
This way, I can scale running the inspections.
I use PostgreSQL as a database, and Redis for Django Q.

## Services
I'm using S3 to upload, store, and serve the uploaded images.
I use the PositionStack API to look up a place from coordinates (place widget),
and Google Cloud Vision API to recognize text and landmarks.

