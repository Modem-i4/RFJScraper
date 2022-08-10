<?php


namespace App\Filters;


class CategoryFilter extends QueryFilter
{
    protected $searchable = [
        'base.name',
    ];

    protected $sortable = [
        'base.name',
        'base.display',
    ];
}
