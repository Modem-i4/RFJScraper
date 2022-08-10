<nav class="navbar navbar-expand-md navbar-light bg-white shadow-sm fixed-top w-100 py-0" style="z-index: 1500">
    <div class="container">

        <a class="navbar-brand" href="{{ url('/') }}">
            @if(Auth::user() != null && Auth::user()->hasRole("redactor"))
            {{ config('app.name', 'RFJScraper') }}
            @else
            App
            @endif
        </a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="{{ __('Toggle navigation') }}">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <!-- Left Side Of Navbar -->
            @if(Auth::user() != null)
                <ul class="navbar-nav mr-auto">
                    @if(Auth::user()->hasRole("redactor"))
                        <li class="nav-item">
                            <a href="/posts" class="text-dark ml-2 d-flex">
                                <h4 class="mdi mdi-floppy mb-0 h4">{{__('other.posts')}}</h4>
                            </a>
                        </li>
                    @endif
                    @if(Auth::user()->hasRole("manager"))
                            <li class="nav-item">
                                <a href="/profiles" class="text-dark ml-2 d-flex">
                                    <h4 class="mdi mdi-folder-account mb-0 h4">{{__('other.profiles')}}</h4>
                                </a>
                            </li>
                            <li class="nav-item">
                                <a href="/categories" class="text-dark ml-2 d-flex">
                                    <h4 class="mdi mdi-filter-menu mb-0 h4">{{__('other.categories')}}</h4>
                                </a>
                            </li>
                    @endif
                    @if(Auth::user()->hasRole("admin"))
                            <li class="nav-item">
                                <a href="/users" class="text-dark ml-2 d-flex">
                                    <h4 class="mdi mdi-account mb-0 h4">{{__('other.users')}}</h4>
                                </a>
                            </li>
                            <li class="nav-item">
                                <a href="/settings" class="text-dark ml-2 d-flex">
                                    <h4 class="mdi mdi-wrench mb-0 h4">{{__('other.settings')}}</h4>
                                </a>
                            </li>
                    @endif
                </ul>
        @endif

        <!-- Right Side Of Navbar -->
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <lang-changer></lang-changer>
                </li>
                <!-- Authentication Links -->
                @guest
                    @if (Route::has('login'))
                        <li class="nav-item">
                            <a class="nav-link" href="{{ route('login') }}">{{ __('other.login') }}</a>
                        </li>
                    @endif

                    @if (Route::has('register'))
                        <li class="nav-item">
                            <a class="nav-link" href="{{ route('register') }}">{{ __('other.register') }}</a>
                        </li>
                    @endif
                @else
                    <li class="nav-item dropdown">
                        <a id="navbarDropdown" class="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" v-pre style="font-size: 0.9rem;">
                            {{ Auth::user()->name }}
                        </a>

                        <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">
                            <a class="dropdown-item" href="{{ route('logout') }}"
                               onclick="event.preventDefault();
                                                     document.getElementById('logout-form').submit();">
                                {{ __('other.logout') }}
                            </a>

                            <form id="logout-form" action="{{ route('logout') }}" method="POST" class="d-none">
                                @csrf
                            </form>
                        </div>
                    </li>
                @endguest
            </ul>
        </div>
    </div>
</nav>
