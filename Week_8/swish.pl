% Tìm min giữa A và B
min(A, B, A) :- A =< B.
min(A, B, B) :- A > B.

% Hàm giải bài toán. Ví dụ: giai_bai_toan(3, 4, 2).
giai_bai_toan(Vx, Vy, Z) :-
    write('Bat dau dong nuoc:'), nl,
    write('  (Vx='), write(Vx), write(', Vy='), write(Vy), write(', Can lay Z='), write(Z), write(')'), nl,
    write('---------------------------------'), nl,
    dong_nuoc(Vx, Vy, Z, 0, 0).


% 1. ĐIỀU KIỆN DỪNG 

% Dừng khi lượng nước ở bình X hoặc bình Y bằng Z
dong_nuoc(_, _, Z, X, Y) :-
    (X =:= Z; Y =:= Z),
    write('---------------------------------'), nl,
    write('KET QUA: Da dong duoc '), write(Z), write(' lit.'), nl,

% 2. Nếu bình Y rỗng thì đổ nước đầy bình Y
dong_nuoc(Vx, Vy, Z, X, Y) :-
    Y =:= 0,
    Y_new is Vy,
    write('1. Binh Y rong -> Do day binh Y'), nl,
    write('   Trang thai: (X='), write(X), write(', Y='), write(Y_new), write(')'), nl,
    dong_nuoc(Vx, Vy, Z, X, Y_new).

% 3. Nếu bình X đầy thì đổ hết nước ra
dong_nuoc(Vx, Vy, Z, X, Y) :-
    X =:= Vx,
    X_new is 0,
    write('2. Binh X day -> Do het nuoc binh X'), nl,
    write('   Trang thai: (X='), write(X_new), write(', Y='), write(Y), write(')'), nl,
    dong_nuoc(Vx, Vy, Z, X_new, Y).

% 4. Đổ từ Y sang X
% Nếu bình Y không rỗng và bình X chưa đầy
dong_nuoc(Vx, Vy, Z, X, Y) :-
    Y > 0, X < Vx,
    Cho_trong is Vx - X,   
    min(Y, Cho_trong, K),  
    X_new is X + K,         
    Y_new is Y - K,        
    
    write('3. Do tu Y sang X (do '), write(K), write(' lit)'), nl,
    write('   Trang thai: (X='), write(X_new), write(', Y='), write(Y_new), write(')'), nl,
    dong_nuoc(Vx, Vy, Z, X_new, Y_new).


% test case
/* 
 giai_bai_toan(3, 4, 2)
 Bat dau dong nuoc:
(Vx=3, Vy=4, Can lay Z=2)
---------------------------------
1. Binh Y rong -> Do day binh Y
Trang thai: (X=0, Y=4)
3. Do tu Y sang X (do 3 lit)
Trang thai: (X=3, Y=1)
2. Binh X day -> Do het nuoc binh X
Trang thai: (X=0, Y=1)
3. Do tu Y sang X (do 1 lit)
Trang thai: (X=1, Y=0)
1. Binh Y rong -> Do day binh Y
Trang thai: (X=1, Y=4)
3. Do tu Y sang X (do 2 lit)
Trang thai: (X=3, Y=2)

KET QUA: Da dong duoc 2 lit.
true
*/

 






























