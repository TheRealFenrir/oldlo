"use strict"

var playersEntered = false;
var scoreEntered = false;

$( document ).ready( function( )
{
    retrieveAndPopulateLeaderboard( );

    retrieveAndPopulateHistory( );

    var getPlayers = new XMLHttpRequest( );
    getPlayers.onreadystatechange = function ( ) {
        if( getPlayers.readyState == 4 && getPlayers.status == 200 )
        {
            var jsonList = JSON.parse( getPlayers.responseText );
            populateGamePlayers( jsonList );
        }
    }

    getPlayers.open( "GET", "cgi-bin/list_players_in_league.py" );
    getPlayers.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" );
    getPlayers.send( );

    $( "#submitGameButton" ).click( function( ) {
        var submitGame = new XMLHttpRequest( );
        submitGame.onreadystatechange = function( ) {
            if( submitGame.readyState == 4 && submitGame.status == 200 )
            {
                // Update the leaderboard
                retrieveAndPopulateLeaderboard( );
                retrieveAndPopulateHistory( );
            }
        };

        submitGame.open( "POST", "cgi-bin/add_game.py" );
        submitGame.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" );
        var submitString = "p1_id=" + $( "#team1Player1" ).val( ) + "&" +
                    "p2_id=" + $( "#team1Player2" ).val( ) + "&" +
                    "p3_id=" + $( "#team2Player1" ).val( ) + "&" +
                    "p4_id=" + $( "#team2Player2" ).val( ) + "&" +
                    "t1_score=" + $( "#team1Score" ).val( ) + "&" +
                    "t2_score=" + $( "#team2Score" ).val( );
        $( "#team1Score" ).val( "" );
        $( "#team2Score" ).val( "" );
        handleScoreChange( );
        submitGame.send( submitString );
    } );

    $( "#addPlayerButton" ).click( function( ) {
        var addPlayer = new XMLHttpRequest( );
        addPlayer.onreadystatechange = function( ) {
            if( addPlayer.readyState == 4 && addPlayer.status == 200 )
            {
                $( "#newPlayerName" ).val( "" );
            }
        };

        addPlayer.open( "POST", "cgi-bin/add_player_temp.py" );
        addPlayer.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" );
        var newPlayerName = $( "#newPlayerName" ).val( );
        addPlayer.send( "name=" + newPlayerName );
    } );

    connectScoreEntryHandlers( );
} );

function retrieveAndPopulateLeaderboard( )
{
    var leaderboard = new XMLHttpRequest( );
    leaderboard.onreadystatechange = function ( ) {
        if( leaderboard.readyState == 4 && leaderboard.status == 200 )
        {
            var jsonList = JSON.parse( leaderboard.responseText );
            populateLeaderboard( jsonList );
        }
    }

    leaderboard.open( "GET", "cgi-bin/list_players_in_league.py" );
    leaderboard.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" );
    leaderboard.send( );
}

function populateLeaderboard( jsonResponse )
{
    $( "#player-table" ).find( "tbody>tr" ).remove();
    $.each( jsonResponse, function( index, obj ) {
        var row = $( "<tr>" );
        var td = $( "<td>" );
        td.html( index + 1 );
        row.append( td );
        var td = $( "<td>" );
        td.html( obj.name );
        row.append( td );
        var td = $( "<td>" );
        td.html( obj.elo );
        row.append( td );

        var table = $( "#player-table" );
        table.append( row );
    } );
}

function retrieveAndPopulatePlayerHistory( )
{
    var leaderboard = new XMLHttpRequest( );
    leaderboard.onreadystatechange = function ( ) {
        if( leaderboard.readyState == 4 && leaderboard.status == 200 )
        {
            var jsonList = JSON.parse( leaderboard.responseText );
            populatePlayerHistory( jsonList );
        }
    }

    leaderboard.open( "GET", "cgi-bin/get_player_history.py" );
    leaderboard.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" );
    leaderboard.send( );
}

function populatePlayerHistory( jsonResponse )
{
    $( "#player-stats-table" ).find( "tbody>tr" ).remove();
    var elo;
    var totalGames = 0;
    var totalLosses = 0;
    var totalWins = 0;
    var totalScored = 0;
    var totalScoredAgainst = 0;
    $.each( jsonResponse, function( obj ) {
        elo = obj.elo
        totalGames += 1;
        if( obj.result = "won" ) {
            totalWins += 1;
            totalScored += 5;
            totalScoredAgainst += 5 - obj.scoreDifference;
        }  
        else
        {
            totalLosses += 1;
            totalScoredAgainst += 5;
            totalScored += 5 - obj.scoreDifference;
        }
    } );

    var row = $( "<tr>" );
    var td = $( "<td>" );
    td.html( elo );
    row.append( td );
    var td = $( "<td>" );
    td.html(totalGames);
    row.append( td );
    var td = $( "<td>" );
    td.html( (totalWins / totalGames) * 100 + '%' );
    row.append( td );
    var td = $( "<td>" );
    td.html( totalScored );
    row.append( td );
    var td = $( "<td>" );
    td.html( totalScoredAgainst );
    row.append( td );
         
    var table = $( "#player-stats-table" );
    table.append( row );
}

function retrieveAndPopulateHistory( )
{
    var history = new XMLHttpRequest( );
    history.onreadystatechange = function ( ) {
        if( history.readyState == 4 && history.status == 200 )
        {
            var jsonList = JSON.parse( history.responseText );
            populateHistory( jsonList );
        }
    }

    history.open( "GET", "cgi-bin/get_league_history.py" );
    history.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" );
    history.send( );
}

function populateHistory( jsonResponse )
{
    $( "#history-table" ).find( "tbody>tr" ).remove();
    $.each( jsonResponse, function( index, obj ) {
        var row = $( "<tr>" );
        var td = $( "<td>" );
        td.html( obj.gameId );
        row.append( td );

        td = $( "<td>" );
        td.html( obj.date );
        row.append( td );

        td = $( "<td>" );
        td.html( obj.player1 );
        row.append( td );

        td = $( "<td>" );
        td.html( obj.player2 );
        row.append( td );

        td = $( "<td>" );
        var scoreText = "5 : " + (5 - obj.scoreDifference);
        td.html( scoreText );
        row.append( td );

        td = $( "<td>" );
        td.html( obj.player3 );
        row.append( td );
        
        td = $( "<td>" );
        td.html( obj.player4 );
        row.append( td );

        var table = $( "#history-table" );
        table.append( row );
    } );
}

function connectScoreEntryHandlers( )
{
    $( "#team1Score" ).keyup( handleScoreChange );
    $( "#team2Score" ).keyup( handleScoreChange );
}

function populateGamePlayers( jsonResponse )
{
    var select = $( "<select>" );

    $.each( jsonResponse, function( index, obj ) {
        var opt = $( "<option value=" + obj.id + ">" + obj.name + "</option>" )
        select.append( opt );
    } );

    select.attr( 'id', 'team1Player1' );
    select.change( handleGamePlayerChange );
    $( "#team1Panel" ).append( select );

    select = select.clone( );
    select.change( handleGamePlayerChange );
    select.attr( 'id', 'team1Player2' );
    $( "#team1Panel" ).append( select );

    select = select.clone( );
    select.change( handleGamePlayerChange );
    select.attr( 'id', 'team2Player1' );
    $( "#team2Panel" ).append( select );

    select = select.clone( );
    select.change( handleGamePlayerChange );
    select.attr( 'id', 'team2Player2' );
    $( "#team2Panel" ).append( select );

    handleGamePlayerChange( );
}

function handleGamePlayerChange( )
{
    var selects = $( "select :selected" );

    var unique = { };
    var uniqueGame = true;
    selects.each( function( name, el ) {
        var player = $( el ).text( );
        if( unique.hasOwnProperty( player ) )
        {
            $( "#expectedScore" ).remove( );
            uniqueGame = false;
        }
        else
        {
            unique[ player ] = "";
        }
    } );

    if( uniqueGame )
    {
        var expectedScore = new XMLHttpRequest( );
        expectedScore.onreadystatechange = function ( ) {
            if( expectedScore.readyState == 4 && expectedScore.status == 200 )
            {
                playersEntered = true;
                if( scoreEntered )
                {
                    enableSubmitButton( );
                }

                var jsonList = JSON.parse( expectedScore.responseText );
                if( $( "#expectedScore" ).length == 0 )
                {
                    var expectedScoreNode = $( "<h3 id='expectedScore'>" );
                    expectedScoreNode.insertBefore( "#submitGameButton" );
                }
                var expectedScoreNode = $( "#expectedScore" );
                expectedScoreNode.text( "Expected score: " + jsonList[0] + "-" + jsonList[1] );
            }
        }

        expectedScore.open( "POST", "cgi-bin/expected_score.py" );
        expectedScore.setRequestHeader( "Content-type", "application/x-www-form-urlencoded" );
        var postString = "p1_id=" + $( "#team1Player1" ).val( ) + "&" +
                    "p2_id=" + $( "#team1Player2" ).val( ) + "&" +
                    "p3_id=" + $( "#team2Player1" ).val( ) + "&" +
                    "p4_id=" + $( "#team2Player2" ).val( )
        expectedScore.send( postString );
    }
    else
    {
        playersEntered = false;
        disableSubmitButton( );
    }
}

function handleScoreChange( )
{
    if( ( $( "#team1Score" ).val( ) != "" ) && ( $( "#team2Score" ).val( ) != "" ) )
    {
        scoreEntered = true;
        if( playersEntered )
        {
            enableSubmitButton( );
        }
    }
    else
    {
        scoreEntered = false;
        disableSubmitButton( );
    }
}

function enableSubmitButton( )
{
    $( "#submitGameButton" ).removeClass( "btn-danger" );
    $( "#submitGameButton" ).addClass( "btn-primary" );
    $( "#submitGameButton" ).removeAttr( "disabled" );
}

function disableSubmitButton( )
{
    $( "#submitGameButton" ).addClass( "btn-danger" );
    $( "#submitGameButton" ).removeClass( "btn-primary" );
    $( "#submitGameButton" ).attr( "disabled", "disabled" );
}
