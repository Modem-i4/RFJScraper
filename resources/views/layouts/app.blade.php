<!doctype html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <!-- CSRF Token -->
    <meta name="csrf-token" content="{{ csrf_token() }}">

    <meta name="user-id" content="{{ Illuminate\Support\Facades\Auth::id() }}">

    @if(Auth::user() != null && Auth::user()->hasRole("redactor"))
    <title>{{ config('app.name', 'RFJScraper') }}</title>
    <link rel="icon" href="{{ URL::asset('/favicon.ico') }}" type="image/x-icon"/>
    @else
    <title>App</title>
    <link rel="icon" href="{{ URL::asset('/favicon-2.ico') }}" type="image/x-icon"/>
    @endif

    <!-- Styles -->
    <link href="{{ asset('css/app.css') }}" rel="stylesheet">

    @include('layouts.headers')
</head>
<body>
    <div id="app">
        @include('layouts.navbar')
        <main style="margin-top: 6em">
            @yield('content')
        </main>
    </div>
</body>
</html>
