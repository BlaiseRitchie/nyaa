google.load("jquery", "1.6.4");
google.setOnLoadCallback(function() {

	$("#searchb").click(function () {
		window.location.href = "/search/" + $("#search").val();
	});

});
