<?php


namespace App\Filters;


class UserFilter extends QueryFilter
{
    protected $searchable = [
        'id',
        'name',
        'email',
        'role',
    ];

    protected $sortable = [
        'id',
        'name',
        'email',
        'role',
        'reg_time',
    ];
}
