## Canada.ca Analytics Experimental Dashboard

A collaborationby CSPS-DIS to create a sweet government website analytics dashboard using hockey sticks and pucks that were nearby.

### Getting/Refreshing the Data

Our friends in GoC built a great analytics page `https://www.canada.ca/en/analytics.html`. So did our friends to the south `https://analytics.usa.gov`. We liked them both so much we felt they belonged together, so through the magic of open source and coffee we built this experiment. It's like a toque. Something nice and fuzzy you put ontop of your thinking bits. 

The exisiting analytics page collects data from a few sites, but we thought maybe if they had a superhero cape they could wear (without having to give up on the clark kent glasses because there are probably design decisions or requirements we dont know about). But why not have both?

A small python script gca-scrape.py grabs and finds the important content from our existing analytics site and generates JSON files which can conform to the expected input of the usa.gov code. The exisiting analytics site goes on without a hiccup and we can build a cool dashboard right from its content.

We used [anaconda](https://www.anaconda.com/download/) to help make things easier on us. To create the data files run the following from an anaconda shell:

```bash
conda create --name gcanalytics python=3.5
activate gcanalytics
cd wheremystufflives/development/gcanalytics/gca-scrape/
gca-scrape.py
```

This will write the data files into the data/can-live/ directory of the dashboard

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
gem install sass
```

* To watch the Sass source for changes and build the stylesheets automatically, run:

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

### Deploying the app

Since the dashboard is just html/js/css you can drop the code on basically any webserver and be off to the races.

If you are developing locally, you can do what we did and run a simple python http server. In a shell run the following in your development directory where this code lives:

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

### Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the Canada, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
