<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use App\Traits\Filterable;

class Post extends Model
{
    use HasFactory, Filterable;
    protected $casts = [
        'important' => 'boolean',
        'images' => 'array',
        'external_links' => 'array',
        'published_at' => 'datetime:d M H:i',
        'categories' => 'array',
        ];
    public $timestamps = false;
}
