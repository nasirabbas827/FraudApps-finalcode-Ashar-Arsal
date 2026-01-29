from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Application, AppReview, Feedback
import re
import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Download required NLTK data (run once)
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('sentiwordnet')
# nltk.download('stopwords')

import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn, sentiwordnet as swn, stopwords

stop_words = set(stopwords.words('english'))

def penn_to_wn(tag):
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None


def analyze_sentiment_sentiwordnet(text):
    if not text.strip():
        print("\n" + "="*60)
        print("REVIEW: (empty)")
        print("RESULT: neutral (0.0000)")
        print("="*60)
        return 'neutral', 0.0

    print("\n" + "="*80)
    print(f"REVIEW: {text}")
    print("="*80)

    tokens = word_tokenize(text.lower())
    tagged = pos_tag(tokens)

    positive_score = negative_score = 0.0
    total_terms = objective_count = 0
    word_details = []

    print(f"{'Word':<15} {'POS':<6} {'PosScore':<10} {'NegScore':<10} {'ObjScore':<10} {'Status'}")
    print("-" * 80)

    for word, tag in tagged:
        if word in stop_words or len(word) < 3:
            continue

        clean_word = re.sub(r'[^\w\s]', '', word)
        if not clean_word:
            continue

        wn_tag = penn_to_wn(tag)
        if not wn_tag:
            continue

        synsets = list(wn.synsets(clean_word, wn_tag))
        if not synsets:
            continue

        synset = synsets[0]
        swn_synset = swn.senti_synset(synset.name())

        pos = swn_synset.pos_score()
        neg = swn_synset.neg_score()
        obj = swn_synset.obj_score()

        status = "Counted" if obj < 1.0 else "Objective"

        if obj < 1.0:
            positive_score += pos
            negative_score += neg
            total_terms += 1

        if obj >= 1.0:
            objective_count += 1

        print(f"{clean_word:<15} {tag:<6} {pos:<10.3f} {neg:<10.3f} {obj:<10.3f} {status}")
        word_details.append((clean_word, tag, pos, neg, obj))

    print("-" * 80)

    if total_terms == 0:
        print("No sentiment-bearing words found → neutral")
        compound_score = 0.0
        sentiment = 'neutral'
    else:
        avg_pos = positive_score / total_terms
        avg_neg = negative_score / total_terms
        compound_score = avg_pos - avg_neg

        if compound_score >= 0.1:
            sentiment = 'positive'
        elif compound_score <= -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        print(f"Total sentiment words  : {total_terms}")
        print(f"Objective/neutral words: {objective_count}")
        print(f"Avg Positive Score     : {avg_pos:.4f}")
        print(f"Avg Negative Score     : {avg_neg:.4f}")
        print(f"Compound Score         : {compound_score:.4f}")
        print(f"Final Sentiment        : {sentiment.upper()}")

    print("="*80 + "\n")

    return sentiment, round(compound_score, 4)



# Landing Page
def index(request):
    apps = Application.objects.all().order_by('-created_at')
    feedbacks = Feedback.objects.all().order_by('-created_at')  # Fetch all feedbacks
    return render(request, 'index.html', {'apps': apps, 'feedbacks': feedbacks})



def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')

    return render(request, 'register.html')

# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


# Logout
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render
from .models import Application, AppReview

@login_required
def dashboard(request):
    # Annotate apps with average sentiment score and order by it (highest first)
    apps = Application.objects.annotate(
        avg_sentiment=Avg('reviews__sentiment_score')
    ).order_by('-avg_sentiment')  # Rank by sentiment

    # Get recent reviews of the logged-in user
    user_reviews = AppReview.objects.filter(user=request.user).order_by('-created_at')[:10]

    context = {
        'apps': apps,
        'user_reviews': user_reviews,
    }
    return render(request, 'dashboard.html', context)

import socket
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Application, AppReview


@login_required
def add_review(request, app_id):
    app = get_object_or_404(Application, id=app_id)

    if request.method == "POST":
        comment = request.POST.get('comment', '').strip()

        # ----------------------------
        # Validation
        # ----------------------------
        if not comment:
            messages.error(request, "Review comment cannot be empty.")
            return redirect('add_review', app_id=app_id)

        if len(comment) < 10:
            messages.error(request, "Review must be at least 10 characters long.")
            return redirect('add_review', app_id=app_id)

        # ----------------------------
        # Sentiment Analysis
        # ----------------------------
        sentiment_label, sentiment_score = analyze_sentiment_sentiwordnet(comment)

        # ----------------------------
        # Fake Review Detection
        # Rule: Same user > 3 reviews on same app
        # ----------------------------
        review_count = AppReview.objects.filter(
            app=app,
            user=request.user
        ).count()

        review_status = 'fake' if review_count >= 3 else 'genuine'

        # ----------------------------
        # IP Address Capture
        # ----------------------------
                # Simulating IP address detection
        ip_address = socket.gethostbyname(socket.gethostname())

        print(ip_address)

        # ----------------------------
        # Save Review
        # ----------------------------
        AppReview.objects.create(
            app=app,
            user=request.user,
            comment=comment,
            sentiment=sentiment_label,
            sentiment_score=sentiment_score,
            review_status=review_status,
            ip_address=ip_address
        )

        if review_status == 'fake':
            messages.warning(
                request,
                "Your review was submitted but flagged as fake due to repeated submissions."
            )
        else:
            messages.success(
                request,
                f"Your {sentiment_label} review has been submitted successfully."
            )

        return redirect('app_detail', app_id=app.id)

    return render(request, 'add_review.html', {'app': app})


# App Detail Page (with reviews)
def app_detail(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    reviews = app.reviews.all().order_by('-created_at')
    avg_score = app.reviews.aggregate(Avg('sentiment_score'))['sentiment_score__avg']

    context = {
        'app': app,
        'reviews': reviews,
        'avg_score': round(avg_score, 3) if avg_score else 0.0,
        'total_reviews': reviews.count(),
    }
    return render(request, 'app_detail.html', context)



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Feedback
from django.contrib import messages

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            Feedback.objects.create(user=request.user, message=message)
            messages.success(request, "Thank you for your feedback!")
        else:
            messages.error(request, "Please write some feedback before submitting.")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
