<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use App\Traits\Filterable;

class Profile extends Model
{
    use HasFactory, Filterable;
    protected $casts = [
        'last_publish' => 'datetime:d M H:i',
        'subscribe' => 'boolean',
        ];
    public $timestamps = false;
}
