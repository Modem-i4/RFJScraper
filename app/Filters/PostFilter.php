<?php


namespace App\Filters;


class PostFilter extends QueryFilter
{
    protected $searchable = [
        'base.id',
        'name',
        'text',
        'base.url',
        'categories',
        'published_at',
    ];

    protected $sortable = [
        'id',
        'published_at',
        'important'
    ];
}
