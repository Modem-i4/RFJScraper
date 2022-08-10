<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use App\Traits\Filterable;

class Category extends Model
{
    use HasFactory, Filterable;
    protected $casts = [
        'display' => 'boolean',
    ];
    public $timestamps = false;
}
