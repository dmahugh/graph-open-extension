<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>graph-open-extension</title>
    <link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/site.css?version=1.02" />
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
</head>

% if displayName:
    <body style="background-color:{{favcolor}}">
% else:
    <body>
% end
    <div class="container homepage-container">
        <h1>Open Extensions Example</h1>
        % if displayName:
            <table class="demo">
                <tr><th>User name:</th><td>{{ displayName }} <button type="button" class="btn btn-default btn-sm" onclick="window.location.href='/logout'">Disconnect</button></td></tr>
                <tr><th>Email domain:</th><td>{{ emaildomain }}</td></tr>
                <tr><th>Favorite color:</th><td>{{ favcolor }}</td></tr>
                <tr><td colspan=2><a href="/?setcolor=blue"><img class="colortile" src="/static/images/blue-thumbnail.png"></a><a href="/?setcolor=green"><img class="colortile" src="/static/images/green-thumbnail.png"></a><a href="/?setcolor=orange"><img class="colortile" src="/static/images/orange-thumbnail.png"></a><a href="/?setcolor=red"><img class="colortile" src="/static/images/red-thumbnail.png"></a><a href="/?setcolor=white"><img class="colortile" src="/static/images/white-thumbnail.png"></a></td></tr>
                % if favcolor:
                    <tr><td colspan=2><img src="/static/images/{{favcolor}}.jpg"></td></tr>
                % end
            </table>
        % else:
            <p><button type="button" class="btn btn-default btn-md" onclick="window.location.href='/login'">Connect</button></p>
        % end
    </div>
    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>
</body>
</html>
