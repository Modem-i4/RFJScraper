<head>
    <title>{{$site}} {{ __('other.post') }}</title>
    <style>
        img {
            max-width: 1200px;
            max-height: 800px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
    </style>
</head>
<body>
@if(!$isInstagramPost)
    <img src="/images/screenshots/{{$uid}}.png">
@else
    @for($i = 0; $i<10; $i++)
        <img src="/images/screenshots/{{$uid}}_{{$i}}.png" alt>
    @endfor
@endif
</body>
