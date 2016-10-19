import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }

        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        /*I made change to add the following #scene id.*/
        #scene .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }

        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }

        #trailer-video {
            width: 100%;
            height: 100%;
        }
        /*I made change to add the following #scene-video id.*/
        #scene-video {
            width: 100%;
            height: 100%;
        }
        
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }

        /*I made change to add the following two classes.*/
        .customized_description_rating {
            background-image: linear-gradient(rgba(255,255,255,0.5),rgba(255,255,255,0.5)), url('2hFONCx.png');
            /*The above trick serves to make the backgroud picture opaque while not affecting the 
            opacity of the text.*/
            background-size: cover; 
            display: inline-block; 
            font-size: 40px; 
            font-family: fantasy; 
            color: rgba(0, 0, 0, 0.5); /*Set the opacity of the text.*/
            height: 70px;
        }
        .customized_description_review {
            display: inline-block; 
            text-align: justify; 
            margin-left: 15px; 
            height: 70px;
            overflow-y: auto;    /* Trigger vertical scroll    */
            overflow-x: hidden;  /* Hide the horizontal scroll */ 
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed for the trailer
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened.
        // I changed the second argument '.movie-tile' to '.click_tr', \
        // so that now we need to click the text I specified to open the trailer.
        $(document).on('click', '.click_tr', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });

        // Pause the video when the modal is closed for the scene
        // The following two blocks of codes are analogous to the above.
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#scene-video-container").empty();
        });
        // Start playing the video whenever the scene modal is opened
        // I changed the second argument '.movie-tile' to '.click_sc', \
        // so that now we need to click the text I specified to open the scene.
        $(document).on('click', '.click_sc', function (event) {
            var sceneYouTubeId = $(this).attr('data-scene-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + sceneYouTubeId + '?autoplay=1&html5=1';
            $("#scene-video-container").empty().append($("<iframe></iframe>", {
              'id': 'scene-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });


        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Scene Video Modal, added by Sheng BI -->
    <div class="modal" id="scene">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="scene-video-container">
          </div>
        </div>
      </div>
    </div>
    
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes, Those Movies that you want to watch again ;-)</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center">
    <img src="{poster_image_url}" width="260" height="342">
    <h3><strong>{movie_title}</strong></h3>
    <!--I added the rating and review for each movie.-->
    <div style="display:flex; margin-left: 8%; margin-right: 8%;">
        <span class = "customized_description_rating">{rating}</span>
        <span class = "customized_description_review">{review}</span>
    </div>

    <!--I now explicitly specify the texts upon which I should click to open the videos.-->
    <div class = "click_tr" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
        <span style = "font-size: 20px;"><em>Click Me for the Trailer</em></span>
    </div>
    <div class = "click_sc" data-scene-youtube-id="{scene_youtube_id}" data-toggle="modal" data-target="#scene">
        <span style = "font-size: 20px;"><em>Click Me for one Famous Scene</em></span>
    </div>    
</div>
'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url for the trailer
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Extract the youtube ID from the url for the famous scene, added by Sheng
        youtube_id_match_scene = re.search(r'(?<=v=)[^&#]+', movie.scene)
        youtube_id_match_scene = youtube_id_match_scene or re.search(r'(?<=be/)[^&#]+', movie.scene)
        scene_youtube_id = youtube_id_match_scene.group(0) if youtube_id_match_scene else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title = movie.title,
            poster_image_url = movie.poster_image_url,
            trailer_youtube_id = trailer_youtube_id,
            # The following three lines integrate the movie specific information into the webpage. 
            scene_youtube_id = scene_youtube_id, 
            rating = movie.rating,
            review = movie.review
        )
    return content

def open_movies_page(movies):
  # Create or overwrite the output file
  output_file = open('fresh_tomatoes.html', 'w')

  # Replace the placeholder for the movie tiles with the actual dynamically generated content
  rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))

  # Output the file
  output_file.write(main_page_head + rendered_content)
  output_file.close()

  # open the output file in the browser
  url = os.path.abspath(output_file.name)
  webbrowser.open('file://' + url, new=2) # open in a new tab, if possible