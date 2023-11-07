<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="Bottle web project template">
        <link rel="icon" href="/static/favicon.ico">
        <title>Project</title>
        <link rel="stylesheet" type="text/css" href="/static/bootstrap.min.css">
        <link rel="stylesheet" href="/static/numpad-light.css"/>
        <script type="text/javascript" src="/static/bootstrap.min.js"></script>
        <script src="/static/numpad.js"></script>
        <style>
            tr td:last-child {
                font-weight:bold;
            }
        </style>
    </head>
    <body style="max-width: 500px;margin: auto;background: white;padding: 10px;">
        <form action="/upload" method="post" enctype="multipart/form-data">
            <div class="form-group">
                <label for="upload">Naloži datoteko</label>
                <input type="file" class="form-control-file" id="upload" name="upload">
                <br><label for="quantity">Količina</label>
                <input type="number" id="quantity" name="quantity" min="1" value=1>
                <input type="submit" value="Naloži" />
            </div>
        </form>
    </body>
</html>