import instaloader
from instaloader import Profile, Instaloader
import time
import json
import os
import shutil


L = instaloader.Instaloader(
    quiet=True,
    dirname_pattern="profiles/{profile}",
    filename_pattern="{date_utc:%Y-%m-%d_%H-%M-%S}_{shortcode}",
    download_comments=True
)



def build_profiles(profiles):
    return [Profile.from_username(L.context, profile) for profile in profiles]

def save_profile_details(details, target):
    os.makedirs(f"profiles/{target}", exist_ok=True)
    filename = f"{target}_details.json"
    file_path = os.path.join("profiles",target,filename)
    with open(file_path,"w") as f:
        json.dump(details,f)

def zip_dir(target):
    shutil.make_archive(target, 'zip', target)

def clean_downloads(target):
    shutil.rmtree(target)
    os.remove(f"{target}.zip")


def scrape(profiles, gui_queue):
    profiles_list = build_profiles(profiles)
    total_profiles = len(profiles_list)
    for i,profile in enumerate(profiles_list):
        details = dict(
            user_id=profile.userid,
            username=profile.username,
            is_private=profile.is_private,
            mediacount=profile.mediacount,
            igtvcount=profile.igtvcount,
            followers=profile.followers,
            followees=profile.followees,
            is_business_account=profile.is_business_account,
            full_name=profile.full_name,
            biography=profile.biography
        )
        for post in profile.get_posts():
            try:
                L.download_post(post, target=profile.username)
            except instaloader.InstaloaderException as e:
                gui_queue.put(str(e))
        
        save_profile_details(details,target=profile.username)
        # zip_dir(profile.username)
        gui_queue.put(f"Profile:{profile.username} -> Downloaded")
        # gui_queue.put(f"Profile:{profile.username} -> Uploading")
        # upload data
        # gui_queue.put(f"Profile:{profile.username} -> Upload Successful")
        # clean_downloads(target=profile.username)
        time.sleep(10)


