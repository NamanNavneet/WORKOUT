import streamlit as st
import pandas as pd
import helper
import pyrebase
from datetime import datetime

def work():
    st.sidebar.title("WORKOUTS")
    user_menu = st.sidebar.radio(
        'Select an Option',
        ('Running Exercises', 'Mat Exercises', 'Stretching', 'Leg Day', 'Yoga', 'Dumbbells', 'Gym Exercise')
    )

    if user_menu == 'Mat Exercises':
        helper.mat()

    if user_menu == 'Stretching':
        helper.stretch()

    if user_menu == 'Leg Day':
        helper.leg()

    if user_menu == 'Yoga':
        helper.yoga()

    if user_menu == 'Running Exercises':
        helper.run()

    if user_menu == 'Dumbbells':
        helper.dumbbells()

    if user_menu == 'Gym Exercise':
        helper.gym()
def feeds():
    all_users = db.get()
    res = []
    # Store all the users handle name
    for users_handle in all_users.each():
        k = users_handle.val()["Handle"]
        res.append(k)
    # Total users
    nl = len(res)
    st.write('Total users here: ' + str(nl))

    # Allow the user to choose which other user he/she wants to see
    choice = st.selectbox('My Collegues', res)
    push = st.button('Show Profile')

    # Show the choosen Profile
    if push:
        for users_handle in all_users.each():
            k = users_handle.val()["Handle"]
            #
            if k == choice:
                lid = users_handle.val()["ID"]

                handlename = db.child(lid).child("Handle").get().val()

                st.markdown(handlename, unsafe_allow_html=True)

                nImage = db.child(lid).child("Image").get().val()
                if nImage is not None:
                    val = db.child(lid).child("Image").get()
                    for img in val.each():
                        img_choice = img.val()
                        st.image(img_choice)
                else:
                    st.info("No profile picture yet. Go to Edit Profile and choose one!")

                # All posts
                all_posts = db.child(lid).child("Posts").get()
                if all_posts.val() is not None:
                    for Posts in reversed(all_posts.each()):
                        st.code(Posts.val(), language='')
def settings():
    nImage = db.child(user['localId']).child("Image").get().val()
    # IMAGE FOUND
    if nImage is not None:
        # We plan to store all our image under the child image
        Image = db.child(user['localId']).child("Image").get()
        for img in Image.each():
            img_choice = img.val()
            # st.write(img_choice)
        st.image(img_choice)
        exp = st.expander('Change Bio and Image')
        # User plan to change profile picture
        with exp:
            newImgPath = st.text_input('Enter full path of your profile imgae')
            upload_new = st.button('Upload')
            if upload_new:
                st.image(newImgPath)
                uid = user['localId']
                fireb_upload = storage.child(uid).put(newImgPath, user['idToken'])
                a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens'])
                db.child(user['localId']).child("Image").push(a_imgdata_url)
                st.success('Success!')
                # IF THERE IS NO IMAGE
    else:
        st.info("No profile picture yet")
        newImgPath = st.text_input('Enter full path of your profile image')
        upload_new = st.button('Upload')
        if upload_new:
            uid = user['localId']
            # Stored Initated Bucket in Firebase
            fireb_upload = storage.child(uid).put(newImgPath, user['idToken'])
            # Get the url for easy access
            a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens'])
            # Put it in our real time database
            db.child(user['localId']).child("Image").push(a_imgdata_url)
def home():
    col1, col2 = st.columns(2)

    # col for Profile picture
    with col1:
        nImage = db.child(user['localId']).child("Image").get().val()
        if nImage is not None:
            val = db.child(user['localId']).child("Image").get()
            for img in val.each():
                img_choice = img.val()
            st.image(img_choice, use_column_width=True)
        else:
            st.info("No profile picture yet. Go to Edit Profile and choose one!")

        post = st.text_input("Let's share my current mood as a post!", max_chars=100)
        add_post = st.button('Share Posts')
    if add_post:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        post = {'Post:': post,
                'Timestamp': dt_string}
        results = db.child(user['localId']).child("Posts").push(post)
        st.balloons()

    # This coloumn for the post Display
    with col2:

        all_posts = db.child(user['localId']).child("Posts").get()
        if all_posts.val() is not None:
            for Posts in reversed(all_posts.each()):
                # st.write(Posts.key()) # Morty
                st.code(Posts.val(), language='')
def table():
    col1, col2 = st.columns(2)
    with col1:
        core = ['Abdominal Crunches','Sit-ups','Butterfly Sit-ups','Flutter Kicks','Scissors','Heel Touch','Knee Crunches','Cross Crunches','Bicycle Crunches','Knee to elbow Crunches','Oblique Crunches',
    'Upper Crunches','Reverse Crunches','V Cruches','Forward Boat Crunches with support','Forward Boat Crunches without support','Sideways Boat Crunches','Alternate Boat Crunches','Knee Raise','Leg Raise',
    'Wipers','Superman Pose','Boat Pose','Twisted Funky Pigeon','Butt Ups','Shoulder Taps','Toe Taps','Mountain Climbers','Froggers','Leg Raise and Hold','Cruch and kick','3 legged Dog Crunches','Thoracic Bridge',
    'Leg lower 2x abductions','Crab Toe Touch','Reverse Kicks','Kick Sets','Inchworms','Russian Twist']
        pnp = ['Plank','Side Plank','Side Jump Plank','Rotating Plank','Toe Touch Plank','Full Pushups','Half Pushups','Side to side Pushups','Pushups-2','Pushups-3']
        core = st.multiselect('Select Core Exercises:', options= core)
        pnp = st.multiselect('Select Core Exercises:', options=pnp)
        add_w = st.button('Share Posts')
    if add_w:
        core_1 = {'CORE WORKOUTS': core}
        pnp_1 = {'PLANK & PUSH-UPS': pnp}
        results = db.child(user['localId']).child("PLANK & PUSH-UPS").push(pnp_1)
        results = db.child(user['localId']).child("CORE WORKOUTS").push(core_1)
        st.balloons()

    with col2:
        all_cs = db.child(user['localId']).child("CORE WORKOUTS").get()
        all_ps = db.child(user['localId']).child("PLANK & PUSH-UPS").get()
        st.write("WORKOUTS")
        if all_cs.val() is not None:
            st.table(all_cs.each()[-1].val())
        if all_ps.val() is not None:
            st.table(all_ps.each()[-1].val())


        ##for history of changes
        ##if all_ps.val() is not None:
            ##for pnps in reversed(all_ps.each()):
                ##st.table(pnps.val())
def Music():
    st.header("Workout Songs List")
    st.write("You Shook Me All Night Long — AC/DC JAM")
    st.write("Take Over Control — Afrojack (feat. Eva Simons)")
    st.write("Addicted to You (David Guetta Remix) — Avicii")
    st.write("Wake Me Up — Avicii")
    st.write("212 — Azealia Banks, Lazy Jay")
    st.write("Harlem Shake — Baauer")
    st.write("Brass Monkey — Beastie Boys")
    st.write("Drunk in Love — Beyonce and JAY Z")
    st.write("Locked Out of Heaven (Sultan + Shepard Remix) — Bruno Mars")
    st.write("Treasure — Bruno Mars")
    st.write("Put Your Hands Where My Eyes Could See — Busta Rhymes")
    st.write("I Need Your Love — Calvin Harris (feat. Ellie Goulding)")
    st.write("Let’s Go (Radio Edit) — Calvin Harris and Ne-Yo")
    st.write("Summer — Calvin Harris ")
    st.write("Sweet Nothing — Calvin Harris (feat. Florence Welch)")
    st.write("Safe and Sound — Capital Cities")
    st.write("Get Lucky (Radio Edit) — Daft Punk (feat. Pharrell Williams and Nile Rodgers)")
    st.write("One More Time — Daft Punk")
    st.write("Titanium — David Guetta (feat. Sia)")
    st.write("Memories — David Guetta (feat. Kid Cudi)")
    st.write("F For You — Disclosure")
    st.write("Latch — Disclosure and Sam Smith")
    st.write("All I Do Is Win — DJ Khaled (feat. T-Pain, Ludacris, Snoop Dogg and Rick Ross)")
    st.write("Turn Down for What — DJ Snake and Lil Jon")
    st.write("Party Up — DMX")
    st.write("Danza Kuduro — Don Omar and Lucenzo")
    st.write("Hold On, We’re Going Home — Drake and Majid Jordan")
    st.write("Burn — Ellie Goulding")
    st.write("The Monster — Eminem and Rihanna")
    st.write("Walking on a Dream (Empire of the Sun)")
    st.write("Call On Me (Radio Edit) — Eric Prydz")
    st.write("American Boy — Estelle and Kanye West")
    st.write("Praise You (Chill Mix) — King Arthur and Michael Meaco")
    st.write("Bad Vibrations — Jesper Jenset")
    st.write("Everlong  — Foo Fighters")
    st.write("Freaks — French Montana and Nicki Minaj")
    st.write("Sad Sad City — Ghostland Observatory")
    st.write("Tongue Tied — Grouplove")
    st.write("Paradise City — Guns N’ Roses")
    st.write("Jump Around — House Of Pain")
    st.write("I Love It — Icona Pop (feat. Charli XCX)")
    st.write("Radioactive (Remix) — Imagine Dragons (feat. Kendrick Lamar)")
    st.write("Marry Me — Jason Derulo")
    st.write("All of Me (Tiesto’s Birthday Treatment Radio Edit) — John Legend, Jason Agel and Tiesto")
    st.write("SexyBack — Justin Timberlake (feat. Timberland)")
    st.write("Suit & Tie — Justin Timberlake (feat. JAY Z)")
    st.write("Take Back the Night — Justin Timberlake ")
    st.write("Higher Love — Kygo and Whitney Houston")
    st.write("Black Widow — Iggy Izalea and Rita Ora")
    st.write("Clique (Album Version) — Kanye West, JAY Z and Big Sean")
    st.write("Mercy (Edited Version) — Kanye West, Big Sean, Pusha T, 2 Chainz")
    st.write("POWER (Album Version) — Kanye West")
    st.write("Dark Horse — Katy Perry and Juicy J")
    st.write("Pursuit of Happiness (Extended Steve Aoki Remix) — Kid Cudi, MGMT, Ratatat, Steve Aoki")
    st.write("Alive (Cash Cash and Kalkutta Remix) — Krewella, Cash Cash and Kalkutta")
    st.write("Summertime Sadness (Cedric Gervais Remix) — Lana Del Rey and Cedric Gervais")
    st.write("Are You Gonna Go My Way — Lenny Kravitz")
    st.write("Outta Your Mind — Lil Jon and LMFAO")
    st.write("Royals — Lorde")
    st.write("Team — Lorde")
    st.write("Y.A.L.A. — M.I.A.")
    st.write("Thrift Shop — Macklemore and Ryan Lewis (feat. Wanz)")
    st.write("Can’t Hold Us — Macklemore and Ryan Lewis (feat. Ray Dalton)")
    st.write("Pon De Floor — Major Lazer and Vybz Kartel")
    st.write("Watch Out For This (Bumaye) — Major Lazer, Busy Signal, The Flexican and FS Green")
    st.write("Animals (Victor Niglio and Martin Garrix Festival Trap Mix) — Martin Garrix and Victor Niglio")
    st.write("The Night Out (A-Trak vs. Martin Rework) — Martin Solveig")
    st.write("Spectrum (Acoustic) — Matthew Koma")
    st.write("Electric Feel — MGMT")
    st.write("4 My People — Missy Elliot (feat. Eve)")
    st.write("Get Your Freak On — Missy Elliot")
    st.write("Hip Hop Hooray — Naughty By Nature")
    st.write("Ride Wit Me (Album Version) — Nelly and City Spud")
    st.write("Pound The Alarm (Edit) — Nick Minaj")
    st.write("Counting Stars — OneRepublic")
    st.write("If I Lose Myself (Alesso vs. OneRepublic) — OneRepublic and Alesso")
    st.write("Million Voices — Otto Knows")
    st.write("Hey Ya! — OutKast")
    st.write("The Way You Move — OutKast (feat. Sleepy Brown)")
    st.write("Happy — Pharrell Williams")
    st.write("Who (Radio Edit) — Tujamo and Plastik Funk")
    st.write("Otherside — Red Hot Chili Peppers")
    st.write("Where Have You Been — Rihanna")
    st.write("Blurred Lines — Robin Thicke, T.I., Pharrell Williams")
    st.write("Walk This Way — Run-D.M.C. (feat. Aerosmith)")
    st.write("What I Got — Sublime")
    st.write("Don’t You Worry Child (Radio Edit) — Swedish House Mafia and John Martin")
    st.write("Greyhound — Swedish House Mafia")
    st.write("One (Your Name) —  Swedish House Mafia and Pharrell Williams")
    st.write("Mr. Brightside — The Killers")
    st.write("Hypnotize — The Notorious B.I.G.")
    st.write("Start Me Up (Remastered) — The Rolling Stones")
    st.write("The Seed (2.0) — The Roots and Cody Chesnutt")
    st.write("Seven Nation Army — The White Stripes")
    st.write("Red Lights — TiestoBlow the Whistle — Too $hort#that")
    st.write("POWER — will.i.am and Justin Bieber")
    st.write("Work Hard, Play Hard — Wiz Khalifa")
    st.write("Clarity (Tiesto Remix) — Zedd (feat. Foxes)")
    st.write("Crash Into Me — Steve Aoki and Darren Criss")





firebaseConfig = {
  'apiKey': "AIzaSyAcj1XrDWhmeEgPQc5QUM-f_hbM3pKPBu0",
  'authDomain': "workout-470b6.firebaseapp.com",
  'projectId': "workout-470b6",
  'databaseURL':'https://workout-470b6-default-rtdb.firebaseio.com/',
  'storageBucket': "workout-470b6.appspot.com",
  'messagingSenderId': "155670458832",
  'appId': "1:155670458832:web:58d4d24ad57e61474ec9d5",
  'measurementId': "G-WPPQ8KWHE0"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()
st.sidebar.title("WELCOME")
choice = st.sidebar.selectbox('login/signup',['Login','Sign up'])
email = st.sidebar.text_input("Enter email:")
password = st.sidebar.text_input("Enter password",type="password")
if choice == "Sign up":
    handle = st.sidebar.text_input("Please input your handle name",value="Default")
    submit = st.sidebar.button("Create my account")

    if submit:
        try:
            user = auth.create_user_with_email_and_password(email,password)
            st.success('Your account is created successfully!')
            st.balloons()
            user = auth.sign_in_with_email_and_password(email, password)
            db.child(user['localId']).child("Handle").set(handle)
            db.child(user['localId']).child("ID").set(user['localId'])
            st.title('Welcome ' + handle)
            st.info('Login via login drop down selection')


        except:
            st.write("TRY AGAIN WITH ANOTHER EMAIL.")


if choice == "Login":
    login = st.sidebar.checkbox('Login')
    if login:
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.title("Welcome")
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            bio = st.radio('Jump to', ['Home','Posts','Workplace Feeds','Customized Workout Table','Settings','Music Area'])
            if bio == "Home":
                work()
            if bio == "Posts":
                home()
            if bio == "Workplace Feeds":
                feeds()
            if bio == "Settings":
                settings()
            if bio == 'Customized Workout Table':
                table()
            if bio == 'Music Area':
                Music()
        except:
            st.header("Incorrect password.")





