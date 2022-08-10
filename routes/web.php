<?php

use App\Http\Controllers\CategoryController;
use App\Http\Controllers\ImageProxyController;
use App\Http\Controllers\LocalizationController;
use App\Http\Controllers\NotificationController;
use App\Http\Controllers\PostController;
use App\Http\Controllers\PresenterController;
use App\Http\Controllers\ProfileController;
use App\Http\Controllers\SettingController;
use App\Http\Controllers\UserController;
use Illuminate\Support\Facades\App;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Facades\Redirect;
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Session;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/
Auth::routes();

if (session()->has('locale')) {
    App::setLocale('en');
}

Route::group(['middleware' => 'role:redactor'], function () {
    Route::redirect('/', 'posts');
    Route::get('posts', [PostController::class, 'index']);
    Route::get('posts/{id}', [PresenterController::class, 'get']);
});
Route::group(['middleware' => 'role:manager'], function () {
    Route::get('profiles', [ProfileController::class, 'index']);
    Route::get('categories', [CategoryController::class, 'index']);
});
Route::group(['middleware' => 'role:admin'], function () {
    Route::get('users', [UserController::class, 'index']);
    Route::get('settings', [SettingController::class, 'index']);
});

Route::prefix('api')->group(function () {
    Route::get('posts', [PostController::class, 'all']);
    Route::post('posts/imp/{id}/{importance}', [PostController::class, 'changeImportance']);
    Route::post('posts/categories/{id}', [PostController::class, 'changeCategories']);
    Route::post('posts/remove/{id}', [PostController::class, 'remove']);
    Route::get('profiles', [ProfileController::class, 'all']);
    Route::post('profiles/watch/{id}/{watched}', [ProfileController::class, 'changeWatch']);
    Route::post('profiles/add', [ProfileController::class, 'add']);
    Route::post('profiles/remove/{id}', [ProfileController::class, 'remove']);
    Route::post('profiles/subscribe/{id}/{subscribed}', [NotificationController::class, 'changeSubscribe']);
    Route::get('users', [UserController::class, 'all']);
    Route::post('users/role/{id}/{newRole}', [UserController::class, 'changeRole']);
    Route::post('users/news/{id}/{newState}', [UserController::class, 'changeNewsReceivers']);
    Route::get('categories', [CategoryController::class, 'all']);
    Route::get('categories/names', [CategoryController::class, 'getNames']);
    Route::post('categories/add', [CategoryController::class, 'add']);
    Route::post('categories/remove/{id}', [CategoryController::class, 'remove']);
    Route::post('categories/display/{id}/{state}', [CategoryController::class, 'changeDisplay']);
    Route::get('settings', [SettingController::class, 'all']);
    Route::post('settings/value/{id}/{newValue}', [SettingController::class, 'save']);
    Route::get('image', [ImageProxyController::class, 'get']);
});

Route::get('set_locale/{locale}', [LocalizationController::class, 'index']);
