echo -e "\n\nTesting empy room waitroom"
curl -X GET "https://localhost:8080/users/tournament/checkwaitingroom/room_1/" -k

echo -e "\n\njoining digarcia"
curl -X POST "https://localhost:8080/users/tournament/addtowaitingroom/room_1/digarcia/" -k

echo -e "\n\njoining mortega"
curl -X POST "https://localhost:8080/users/tournament/addtowaitingroom/room_1/mortega/" -k

echo -e "\n\nchecking status"
curl -X GET "https://localhost:8080/users/tournament/checkwaitingroom/room_1/" -k

echo -e "\n\nset digarcia ready to play"
curl -X POST "https://localhost:8080/users/tournament/readytoplay/room_1/digarcia/" -k

echo -e "\n\nset incorrect username ready to play"
curl -X POST "https://localhost:8080/users/tournament/readytoplay/room_1/pepe/" -k

echo -e "\n\nchecking status"
curl -X GET "https://localhost:8080/users/tournament/checkwaitingroom/room_1/" -k

echo -e "\n\nset digarcia ready to play"
curl -X POST "https://localhost:8080/users/tournament/readytoplay/room_1/mortega/" -k

echo -e "\n\nchecking status which actually makes the torunament start as eveyone is ready to play"
# Right now the logiv is that when it is checked and the n_players is 2, 4, 8 o 16 and they are all ready to play the tournament starts. It is a bit weird, maybe this logic should be somewhere else, but all users will be sending this petition all the time, so it should be fine
curl -X GET "https://localhost:8080/users/tournament/checkwaitingroom/room_1/" -k
sleep 0.5

echo -e "\n\nchecking status again"
curl -X GET "https://localhost:8080/users/tournament/checkwaitingroom/room_1/" -k

echo -e "\n\nget state of the tournament (tree of confrontation)"
#This should be only for visualization of the tree on the user side
curl -X GET "https://localhost:8080/users/tournament/getstate/room_1/" -k

echo -e "\n\ndigarcia requests details about their game so game it connects to the game"
#This would be from digarcia's javascrip
curl -X GET "https://localhost:8080/users/tournament/getgame/room_1/digarcia/" -k

echo -e "\n\nmortega requests details about their game so game it connects to the game"
#This would be from mortega's javascrip
curl -X GET "https://localhost:8080/users/tournament/getgame/room_1/mortega/" -k

echo -e "\n\nget state of the tournament (tree of confrontation)"
#This should be only for visualization of the tree on the user side
curl -X GET "https://localhost:8080/users/tournament/getstate/room_1/" -k

echo -e "\n\ngame finishes, digarcia wins"
#IMPORTANT: this is only for this scrip, in general the end of game is triggered within the server from GamaManager stop_game doing tournament_manager.stop_game("room_1", "digarcia", "mortega")
curl -X GET "https://localhost:8080/users/tournament/stopgame/room_1/digarcia/mortega/" -k

echo -e "\n\nget state of the tournament (tree of confrontation)"
#This should be only for visualization of the tree on the user side
curl -X GET "https://localhost:8080/users/tournament/getstate/room_1/" -k


echo -e "\n\nNEW ROOM WITH 4 PLAYERS"

echo -e "\n\njoining digarcia"
curl -X POST "https://localhost:8080/users/tournament/addtowaitingroom/room_2/digarcia/" -k

echo -e "\n\njoining mortega"
curl -X POST "https://localhost:8080/users/tournament/addtowaitingroom/room_2/mortega/" -k

echo -e "\n\njoining acaravan"
curl -X POST "https://localhost:8080/users/tournament/addtowaitingroom/room_2/acaravan/" -k

echo -e "\n\njoining alaguila"
curl -X POST "https://localhost:8080/users/tournament/addtowaitingroom/room_2/alaguila/" -k

echo -e "\n\nset digarcia ready to play"
curl -X POST "https://localhost:8080/users/tournament/readytoplay/room_2/digarcia/" -k

echo -e "\n\nset mortega ready to play"
curl -X POST "https://localhost:8080/users/tournament/readytoplay/room_2/mortega/" -k

echo -e "\n\nset acaravan ready to play"
curl -X POST "https://localhost:8080/users/tournament/readytoplay/room_2/acaravan/" -k

echo -e "\n\nset alaguila ready to play"
curl -X POST "https://localhost:8080/users/tournament/readytoplay/room_2/alaguila/" -k

echo -e "\n\nchecking status which actually makes the torunament start as eveyone is ready to play"
# Right now the logiv is that when it is checked and the n_players is 2, 4, 8 o 16 and they are all ready to play the tournament starts. It is a bit weird, maybe this logic should be somewhere else, but all users will be sending this petition all the time, so it should be fine
curl -X GET "https://localhost:8080/users/tournament/checkwaitingroom/room_2/" -k
sleep 0.5

echo -e "\n\nget state of the tournament (tree of confrontation)"
#This should be only for visualization of the tree on the user side
curl -X GET "https://localhost:8080/users/tournament/getstate/room_2/" -k

echo -e "\n\ndigarcia requests details about their game so game it connects to the game"
#This would be from digarcia's javascrip
curl -X GET "https://localhost:8080/users/tournament/getgame/room_2/digarcia/" -k

echo -e "\n\nmortega requests details about their game so game it connects to the game"
#This would be from mortega's javascrip
curl -X GET "https://localhost:8080/users/tournament/getgame/room_2/mortega/" -k

echo -e "\n\nacaravan requests details about their game so game it connects to the game"
#This would be from acaravan's javascrip
curl -X GET "https://localhost:8080/users/tournament/getgame/room_2/acaravan/" -k

echo -e "\n\nalaguila requests details about their game so game it connects to the game"
#This would be from alaguila's javascrip
curl -X GET "https://localhost:8080/users/tournament/getgame/room_2/alaguila/" -k

echo -e "\n\nget state of the tournament (tree of confrontation)"
#This should be only for visualization of the tree on the user side
curl -X GET "https://localhost:8080/users/tournament/getstate/room_2/" -k

echo -e "\n\ngame finishes, digarcia wins"
#IMPORTANT: this is only for this scrip, in general the end of game is triggered within the server from GamaManager stop_game doing tournament_manager.stop_game("room_1", "digarcia", "mortega")
curl -X GET "https://localhost:8080/users/tournament/stopgame/room_2/digarcia/mortega/" -k

echo -e "\n\nget state of the tournament (tree of confrontation)"
#This should be only for visualization of the tree on the user side
curl -X GET "https://localhost:8080/users/tournament/getstate/room_2/" -k

echo -e "\n\ndigarcia requests new game should return to wait as the other match is still going"
#This would be from digarcia's javascrip
curl -X GET "https://localhost:8080/users/tournament/getgame/room_2/digarcia/" -k

echo -e "\n\ngame finishes, acaravan wins"
#IMPORTANT: this is only for this scrip, in general the end of game is triggered within the server from GamaManager stop_game doing tournament_manager.stop_game("room_1", "digarcia", "mortega")
curl -X GET "https://localhost:8080/users/tournament/stopgame/room_2/acaravan/alaguila/" -k

echo -e "\n\nget state of the tournament (tree of confrontation)"
#This should be only for visualization of the tree on the user side
curl -X GET "https://localhost:8080/users/tournament/getstate/room_2/" -k

echo -e "\n\ndigarcia requests new game should return the game as the other match is finished"
#This would be from digarcia's javascrip
curl -X GET "https://localhost:8080/users/tournament/getgame/room_2/digarcia/" -k

echo -e "\n\nmortega requests new game should not give him a game as he lost to digarcia"
curl -X GET "https://localhost:8080/users/tournament/getgame/room_2/mortega/" -k

echo -e "\n\nacaravan request new game which he gets as he should play against digarcia"
curl -X GET "https://localhost:8080/users/tournament/getgame/room_2/acaravan/" -k

echo -e "\n\nget state of the tournament (tree of confrontation)"
#This should be only for visualization of the tree on the user side
curl -X GET "https://localhost:8080/users/tournament/getstate/room_2/" -k

echo -e "\n\ndigarcia wins"
curl -X GET "https://localhost:8080/users/tournament/stopgame/room_2/digarcia/acaravan/" -k

echo -e "\n\nget state of the tournament (tree of confrontation)"
#This should be only for visualization of the tree on the user side
curl -X GET "https://localhost:8080/users/tournament/getstate/room_2/" -k




