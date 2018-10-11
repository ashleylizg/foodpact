
## Static assets

Eventually when we're up and running with Flask, there'll still be a `static/` folder with `css/` and `js/` below it.

That's because this stuff doesn't change. Flask will serve that folder's contents without executing any Python.

Right now technically the `.html` files are static too so they're in here.

#### Serving to the browser

Make this folder the `pwd` (present working directory) in Powershell then start a simple server with Python.

```
cd foodpact
cd static
python -m http.server
```

Then Powershell will say where the files are being served. If it says `http://0.0.0.0:8000`, you should really do `http://localhost:8000` though.

When you go there, `index.html` will load at the root.

For anything not named `index.html` you'll have to specify like `http://localhost:8000/name-of-the-page-here.html`.

When you want to kill your server do `Ctrl+C` - you don't need to do this when you change stuff though!

#### Note on caching

Since these are all static assets, Google Chrome (or whatever browser) may try to cache them.

If you've changed something but the changes aren't reflected in the browser, you should clear the cache to see.

With your Developer Tools open (`F12` key will do it), hold the Reload button in Chrome. You'll see something like `Empty cache & hard reload` you can click.

When things load after that they should be good.

#### Bootstrap grid system

To work with Bootstrap, you should understand your main content typically needs to be in a `div.container`.

Want to have things in multiple columns? In order to be nice and responsive across devices, you should know about the grid system.

```
<div class="container">
    <div class="row">
        <div class="col-md-6">
            <p>I'm in column 1</p>
        </div>
        <div class="col-md-6">
            <p>I'm in column 1</p>
        </div>
    </div>
</div>
```

On a laptop or tablet, you'd have 2 columns side-by-side, splitting the page body 50/50. That's because you can have up to 12 "columns" in a row.

But on mobile these columns would be on top of each other.

Generally, you can stick to using `<div class="col-md-{{NUMBER HERE}}">` for everything. Usually I do.

You can read more about Bootstrap's [**grid system here**](https://getbootstrap.com/docs/4.0/layout/grid/) but you really don't have to know much more.

#### Bootstrap components and examples

There is great documentation of all Bootstrap's components available to you, with little snippets of HTML for using them.

[**Find that here**](https://getbootstrap.com/docs/4.0/components/alerts/) - this is why you use it, to have all this decent-looking stuff out-of-the-box.

Better yet, find a whole [**page of examples here**](https://getbootstrap.com/docs/4.0/examples/) with code.

#### Color theme

Later, you can use a website called Bootswatch to change the color theme.

They have a bunch of variants of Bootstrap with different colors preloaded than the defaults.

It's generally tough to do this on your own because *sooooo* much CSS makes up the framework to begin with.
