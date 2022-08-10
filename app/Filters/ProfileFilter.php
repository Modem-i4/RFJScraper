<?php


namespace App\Filters;


class ProfileFilter extends QueryFilter
{
    protected $searchable = [
        'profiles.id',
        'name',
        'profiles.url',
    ];

    protected $sortable = [
        'id',
        'name',
        'watched',
        'total_posts',
        'last_publish',
    ];
}
