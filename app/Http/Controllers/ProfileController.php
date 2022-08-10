<?php

namespace App\Http\Controllers;


use App\Repositories\ProfileRepository;

class ProfileController extends Controller
{
    private $repos;
    public function __construct()
    {
        $this->middleware('auth');

        $this->repos = app(ProfileRepository::class);
    }
    public function index() {
        return view('admin.profiles');
    }
    public function all()
    {
        return $this->repos->getAllWithPaginateAndFiltering();
    }
    public function changeWatch($id, $checked)
    {
        return $this->repos->changeWatch($id, $checked == 'true');
    }
    public function remove($id)
    {
        return $this->repos->remove($id);
    }
    public function add() {
        $url = request('url');
        #$url = 'https://facebook.com/michaela.grubesa';
	//exec("sudo python3 ../app/RFJScraper/scrapers/ProfileScraper/ProfileScraper.py $url 2>&1", $output);
		exec("python ../app/RFJScraper/scrapers/ProfileScraper/ProfileScraper.py $url 2>&1", $output);
        if($output[0] === "Success")
            return response('Success', 200);
        elseif ($output[0] === "Already in db") {
            return response('Already in db', 400);
        }
        else {
            return response("Parse or server error. Try later", 500);
        }
    }
}
