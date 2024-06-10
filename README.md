# Book Review Aggregator and Price Comparison Website

As a part of our undergraduate final project, we built a Django webiste for book enthusiasts. This book website's goal is to give people a place online where they can read and post book reviews, express their ideas and opinions, and find new books to read. Users can discover, compare and review books. The main feature of this site is the ability to compare book prices and reviews from different sites. Users can search for books by keywords and browse different categories and genres. Once you've found a book that interests you, you can view the book's details, including the book's cover, author, publisher, and synopsis. You can also check book prices and availability at various online retailers. Apart from the price comparison, this site also offers userreviews from various websites. Users can read and write reviews of books they read, and can also rate books using a star system. The site collects reviews from various sources such as Goodreads, Amazon, and Barnes & Noble to give users a comprehensive picture of the overall reviews. This site aims to improve users' book buying and reading experience by providing one-stop information about books.

## To run the project:
You need to create virtual environment in vscode for running the project. DO NOT CREATE VENV INSIDE PROJECT FOLDER
In terminal do the following:-

1. Create a venv: py -m venv venvname (OR) python -m venv venvname
2. Activate it with : Scripts/activate
3. cd venvname -> (install django) -> pip install django -> (install Pillow) -> pip install Pillow

4. Download git and inside git bash set the global username(just your name) and email id(the one which is linked to github) (watch a tutorial if you want) -- you can open gitbash terminal inside vscode after opening the terminal look for the top right corner of the terminal and you'll find a dropdown and add a git bash terminal
5. Clone the repo with url inside git bash only -- no need to download zip etc etc. (git clone url foldername) 
6. Run project 

7. If changes made to code then commit them: 

---> Create a gitignore file(google it up) and add venvname/ to it so it wont be uploaded to github -- eg. venv1/ -- slash is imp

      Commit after creating gitignore
      (i'm not sure whether to run git init command or not -- search it up)
         { For committing changes to github repo} 
            1. git status
            2. git add *
            3. git commit -m "Update file." --> Relevant message is mandatory while committing
            4. git remote
            5. git remote -v
            6. git branch
            7. git push origin master
            8. {if error in above command} -- run: git push -f origin master


