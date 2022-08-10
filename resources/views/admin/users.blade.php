@extends('layouts.app')

@section('content')
    <section class="">
        <div class="container-fluid">
            <div class="mt-3 mb-3 bg-white rounded">
                <users-table
                :user_id="{{Auth::id()}}"></users-table>
            </div>
        </div>
    </section>

@endsection
