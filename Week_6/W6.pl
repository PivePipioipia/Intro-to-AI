/*
Nguyễn Hồng Yến - 23280099 
*/

parent(marry, bill).
parent(tom, bill).
parent(tom, liz).
parent(bill, ann).
parent(bill, sue).
parent(sue, jim).
woman(marry).
man(tom).
man(bil).
woman(liz).
woman(sue).
woman(ann).
man(jim).


/*
Câu 1:
 a. ?- parent(jim, X)
?- parent(jim, X).
false.

 b. ?- parent(X, jim)
?- parent(X, jim).
X = sue.

 c. ?- parent(marry, X), parent(X, Y).
?- parent(marry, X), parent(X, Y).
X = bill,
Y = ann ;
X = bill,
Y = sue.

 d. ?- parent(marry, X), parent(X, Y), parent(Y, jim).
?- parent(marry, X), parent(X,Y), parent(Y,jim).
X = bill,
Y = sue.

Câu 2: Viết các mệnh đề Prolog diễn tả các câu hỏi liên quan đến quan hệ parent.
 a. Ai là cha mẹ của Bill?
?- parent(X, bill).
X = marry ;
X = tom.
/* Cha của bill là tom, mẹ của bill là marry */

b. Marry có con không?
?- parent(marry, X).
X = bill.
/*Con của marry là bill */

c. Ai là ông bà (grandparent) của Sue?
?- parent(Y, sue), parent(X,Y).
Y = bill,
X = marry ;
Y = bill,
X = tom.

/* Ông của sue là tom, mẹ của sue là marry */

/* Quan hệ diffirent để trả lời câu hỏi Ann là chị em gái của Sue */
sister(X,Y):-parent(Z,X), parent(Z,Y), woman(X), X\=Y.

?- sister(X, sue).
X = ann ;
false.

*/