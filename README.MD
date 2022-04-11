# MyStable

## :racehorse: Application to help you:

#### For stable owners:

- manage your stable
- get in touch with vets in your neighbourhood
- get in touch with farriers

#### For vets:

- manage your patients
- fast contact with stable or horse owners
- plan your visits and share them with owners
- cooperate with farriers

#### For farriers

- manage your visits accordingly to your routes
- share routes and day plan with owners and vets
- cooperate with vets
- stay in touch with owners

## Landing Page

Short story about why is this application good and why should someone use it.

### Navbar should lead to:

:church: :horse: If user logged in as stable owner:

- list of farriers
- list of vets
- if user logged in the Stable button should redirect to the stable, if user is not logged in Stable button should redirect to log in page


:ambulance: :horse: If user logged in as vet:

- list of farriers
- list of stables that user works with
- same thing should happen for non logged users as in case of stable owners


:horse: :shoe: If user logged in as farrier:

- list of vet that user works with
- list of stables user works with
- same thing should happen for non logged user as in case of owners and vets

**AT THE RIGHT END OF NAVBAR SHOULD BE A LOGIN BUTTON !!!**

## Login page

This should be a simple form to log in. Beneath login form is required a question to not yet registered users with
link to registration form.


## Registration form

Should be as simple as possible.

**Fields:**

- First name
- Last name
- Select for occupation Owner, Vet, Farrier.
- e-mail should be used as log in nick
- password
- password repeat

## User is logged in what next?

**If user logged in as:**

Stable owner:

Stable owner is redirected to page with horse pictures that are part of the stable.

**A place for add new horse button is to be found.**

Fields in form for adding new horse:

- Name
- Photo
- Breed
- Parents if known if not known there should be an option or checkbox for unknown
- horse birthdate
- location pf stall in stable



There should be an information about upcoming vaccinations for horses to order them in advance.

*After clicking on a horse user should be redirected to page of a specific horse.*

On horse detail view:
- information about horse name, date of birth, age, breed, parents etc.
- Feeding schema
- Training plan
- Dedicated farrier
- Dedicated vet

For information there should be a dedicated form for creating and editing.

When it comes to training plan the for should have all days of the week in it, but one can check a checkbox named DAY OFF.


Vets list:

- An optional photo of a vet must be visible, if there is none than a default graphic should be displayed.
- phone number under the photo
- after clicking at vets photo user is redirected to vet profile where one can read opinions about vet see all stables the vet works with etc.
- availability
- information about when will the vet be in neighbourhood
