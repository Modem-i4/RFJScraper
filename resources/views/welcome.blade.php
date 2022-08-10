@extends('layouts.app')

@section('content')
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">{{ __('other.dashboard') }}</div>

                    <div class="card-body">
                        @if (session('status'))
                            <div class="alert alert-success" role="alert">
                                {{ session('status') }}
                            </div>
                        @endif

                        <div>{{__('other.logged_in')}}</div>
                        <div>{{__('other.wait_for_confirm')}}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
@endsection
