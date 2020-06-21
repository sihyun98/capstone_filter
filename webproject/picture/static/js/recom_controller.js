$(document).ready(function () {
    // $('#bell').addClass('oldColor');

    // $('#blah1').on('load', function () {
    //     $('#bell').removeClass('oldColor');
    //     $('#bell').addClass('newColor');
    //     // $('#bell').toggleClass('newColor', 'oldColor');
    // });

    // $('#xbutton').click(function () {
    //     $('#bell').toggleClass('oldColor', 'newColor');
    // });

    /////////// HERE
    var loading = $('<div id="preloader"><div class="filter-load"></div></div>').appendTo(document.body).hide();

    $(window)	
    .ajaxStart(function(){
        loading.show();
    })

    .ajaxStop(function(){
        loading.hide();
    });
    ///////////////

    $("#reco_tab").click(() => {

        var inputary = new Array();
        inputary.push(document.getElementById('ex_filename1').files[0]);
        inputary.push(document.getElementById('ex_filename2').files[0]);
        inputary.push(document.getElementById('ex_filename3').files[0]);
        
        var formData = new FormData();
    
        for (var i = 0; i < 3; i++) {
            if (inputary[i] != '') {
                formData.append('input' + i, inputary[i]);
            }
        }
        
        $.ajax({
            type: "POST",
            ContentType: 'application/json',
            url: "http://127.0.0.1:8000/recommend/",
            data: formData,
            processData: false,
            contentType: false,

            success: function (data) {
                // alert("success");
                for (var i = 0; i < 30; i++) {
                    var infodata = data['info'];
                    var infoline = ''
                    for (infokey in infodata) {
                        if (infokey == i) {
                            var infoval = infodata[infokey];
                            infoline += '<div class="col-12 col-md-6 col-lg-4"><div class="single-post wow fadeInUp" data-wow-delay="0.1s"><div class="post-thumb">';
                            for (value in infoval) {
                                if (value == 'url') {
                                    infoline += '<img src="' + infoval[value] + '" data-target="#layerpop" data-toggle="modal"' + 'onclick="pickimage(\'' + infoval[value] + '\');"' + '></div>';
                                } //onclick="pickimage('{{v}}');"
                                else if (value == 'user') {
                                    infoline += '<div class="post-content"><div class="post-meta d-flex"><div class="post-author-date-area d-flex"><div class="post-author"><a href="#">' + infoval[value] + '</a></div>';
                                }
                                else if (value == 'date') {
                                    infoline += '<div class="post-date"><a href="#">' + infoval[value] + '</a></div></div>';
                                }
                                else if (value == 'likes') {
                                    infoline += '<div class="post-comment-share-area d-flex"><a href="#"><div class="post-favourite"><i class="fa fa-heart-o" aria-hidden="true"></i>' + infoval[value] + '</a></div>';
                                }
                                else if (value == 'comments') {
                                    infoline += '<div class="post-comments"><a href="#"><i class="fa fa-comment-o" aria-hidden="true"></i>' + infoval[value] + '</a></div>';
                                }
                                else if (value == 'pageURL') {
                                    infoline += '<div class="post-share"><a href="' + infoval[value] + '"><i class="fa fa-share-alt" aria-hidden="true"></i></a></div></div></div></div></div></div>';
                                }
                            }
                            $('#pic_info').prepend(infoline)
                        }
                    }
                }
            },
            failure:
                function (err) {
                    console.log(err);
                },
            error: function (request, status, error) {
                alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            }
        });
    });



    document.getElementById('search-submit').onsubmit = function() {
        var sh_input = document.getElementById('search-anything').value
        $.ajax({
            type: "GET",
            ContentType: 'application/json',
            url: "http://127.0.0.1:8000/search/",
            data: {sh_input: sh_input},
            dataType: "json",
            success: function (data) {
                for (var i = 0; i < 30; i++) {
                    var infodata = data['searched'];
                    var infoline = ''
                    for (infokey in infodata) {
                        if (infokey == i) {
                            var infoval = infodata[infokey];
                            infoline += '<div class="col-12 col-md-6 col-lg-4"><div class="single-post wow fadeInUp" data-wow-delay="0.1s"><div class="post-thumb">';
                            for (value in infoval) {
                                if (value == 'url') {
                                    infoline += '<img src="' + infoval[value] + '" data-target="#layerpop" data-toggle="modal"' + 'onclick="pickimage(\'' + infoval[value] + '\');"' + '></div>';
                                } //onclick="pickimage('{{v}}');"
                                else if (value == 'user') {
                                    infoline += '<div class="post-content"><div class="post-meta d-flex"><div class="post-author-date-area d-flex"><div class="post-author"><a href="#">' + infoval[value] + '</a></div>';
                                }
                                else if (value == 'date') {
                                    infoline += '<div class="post-date"><a href="#">' + infoval[value] + '</a></div></div>';
                                }
                                else if (value == 'likes') {
                                    infoline += '<div class="post-comment-share-area d-flex"><div class="post-favourite"><a href="#"><i class="fa fa-heart-o" aria-hidden="true"></i>' + infoval[value] + '</a></div>';
                                }
                                else if (value == 'comments') {
                                    infoline += '<div class="post-comments"><a href="#"><i class="fa fa-comment-o" aria-hidden="true"></i>' + infoval[value] + '</a></div>';
                                }
                                else if (value == 'pageURL') {
                                    infoline += '<div class="post-share"><a href="' + infoval[value] + '"><i class="fa fa-share-alt" aria-hidden="true"></i></a></div></div></div></div></div></div>';
                                }
                            }
                            $('#pic_info').prepend(infoline)
                        }
                    }
                }
                $(".tab ul li").removeClass('on');
                $(".tab .conBox").removeClass('on');
                $("#con2").addClass('on');
                $("#conc2").addClass('on');
            },
            failure:
                function (err) {
                    console.log(err);
                },
            error: function (request, status, error) {
                alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            }
        });
        return false;
    };
});