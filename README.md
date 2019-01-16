## Canada.ca Analytics Experimental Dashboard

An alpha collaboration by CSPS Digital Academy to create a sweet government website analytics dashboard using hockey sticks and pucks that were nearby. This is a work in progress.

Our friends in GoC built a great analytics page `https://www.canada.ca/en/analytics.html`. So did our friends to the south `https://analytics.usa.gov`. We liked them both so much we felt they belonged together, so through the magic of open source and coffee we built this experiment. It's like a toque. Something nice and fuzzy you put on top of your thinking bits. 

### Tools and Technology

The experimental apps here are built on the following stack:

* The dashboard uses HTML, [SASS](http://sass-lang.com/), JS, [D3](https://d3js.org/) and the launchpad uses HTML, JS, CSS, [jQuery](https://jquery.com/), [Metro4](https://metroui.org.ua/index.html)
* The data is all JSON files, we harvest the data from our exisiting analytics site with Python 3
* The server-side is an [Azure](https://azure.microsoft.com/en-ca/) cloud running an [Ubuntu VM](https://www.ubuntu.com/), [Python 3](https://www.python.org/downloads/release/python-370/), [Flask](http://flask.pocoo.org/), and [nginx](https://www.nginx.com/)
* We automate our deploys with crontab and [pm2](https://pm2.io/doc/)

> Note: The hard part here really isn't the dashboard or apps we can build with the data - the hard part is getting everyone standardized on one tracking system across the whole landscape. This is an orginizational challenge which will need the help a many talented folks across GoC. We just wanted to demo what we can do if we had this content in easily usable forms. It's easier to share a vision when you can touch and see something. We hope this inspires you too.

### Getting/Refreshing the Data

The exisiting analytics page collects data from a few sites, but we thought maybe if they had a superhero cape they could wear (without having to give up on the clark kent glasses because there are probably design decisions or requirements we dont know about) it would be great. But why not have both?

A small python script gca-scrape.py grabs and finds the important content from our existing analytics site and generates JSON files which can conform to the expected input of the usa.gov code. The exisiting analytics site goes on without a hiccup and we can build a cool dashboard right from its content.

We used [anaconda](https://www.anaconda.com/download/) to help make things easier on us developing locally. To create the data files run the following from an anaconda shell:

```bash
conda create --name gcanalytics python=3.5
activate gcanalytics
cd wheremystufflives/development/gcanalytics/gca-scrape/
gca-scrape.py
```

This will write the data files into the data/can-live/ directory of the dashboard. In the live version of the dashboard we schedule a small cron job to get our data on a schedule. 

### Building the Stylesheets

* Install [Sass](http://sass-lang.com/):
* If you are on windows without make, just directly use sass

```bash
cd wheremystufflives/development/gcanalytics/gca-dashboard/
sass sass/public_analytics.css.scss:sass/public_analytics.css
```
This will create the css files you need. When your testing is done, move htem into the css directory

* Assuming you have make, to watch the Sass source for changes and build the stylesheets automatically, run:

```bash
make watch
```

* To compile the Sass stylesheets once, run:

```bash
make clean all
```

or:

```bash
# -B tells make to run even if the .css file exists
make -B
```

### Updating code and commit to repo

* Switch to dev branch, get changes

```bash
git checkout temp_branch
git pull
```

* Make your changes to templates/styles
* Rebuild stylesheets (see above)

```bash
cd wheremystufflives/development/gcanalytics/gca-dashboard/
sass sass/public_analytics.css.scss:sass/public_analytics.css
```

* If your stylesheets look good, go ahead and copy them into the static/whatmyappiscalled/css/ of the app you're modifying. If you're feeling brave, you can just write out the files to the static directory from sass
* Test changes locally with anaconda in (base) by launching an ananconda terminal window

```bash
cd wheremystufflives/development/gcanalytics/
python application.py
```

* The site should now serve on localhost:5000
* Make sure everything works as you expect, then send it into the repo

```bash
git add .
git commit -m "update msg"
git push
```

### Deploying the app

* Have your project lead merge the temp branch into master
* Deploy master branch code by logging into your cloud instance vm

```bash
 ssh myusername@mydomain.wherever
 cd ~/gcanalytics/gca-scrape
 python3 gca-scrape.py
 cd ~
 sh update_app.sh
 logout
 ```

Since the dashboard is essentially just html/js/css at it's heart, you can drop the code on basically any webserver with minimal edits and be off to the races.

If you are developing locally, you can do what we did during our initial sprint and run a simple python http server. We started this entirely offline, and then made it into a Flask app when we got closer to an alpha version. In a shell run the following in your development directory where this code lives:

```bash
cd wheremystufflives/development/ # gcanalytics folder is here
python -m http.server
```

You should then be able to view the dashboard on `localhost:8000/gcanalytics/`

If you want to have data refresh as the exisiting site updates all you need to do is schedule the gca-scrape.py using your method of choice.

### Get a shareable PNG or PDF

Sometimes you just cant open or see the site on your device. Fear not, you can share the content in image or pdf form by using wkhtmltopdf

* Install [wkhtmltopdf](https://wkhtmltopdf.org/):

To generate image or pdf of the dashboard from the shell you can do the following:

```bash
cd wheremystufflives/development/gcanalytics/gca-dashboard/demo/
wkhtmltopdf -s "Letter" -O "Landscape" http://localhost:8000/gcanalytics/gca-dashboard/demo/ gcanalytics.pdf
wkhtmltoimage http://localhost:8000/gcanalytics/gca-dashboard/demo/ gcanalytics.png
```

The assets should appear in the demo folder and you can use them how you like. 

Note: Depending on the charts you use, you may run into svg issues. But this isn't a core part of our experiment, just an example that you could generate reports/assets that you can share with folks who dont want the web-enabled version.

### Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the Canada, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
