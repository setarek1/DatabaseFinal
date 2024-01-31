-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(0, 'dollar', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(1, 'toman', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(2, 'lire', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(3, 'pound', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(4, 'euro', 10, 10);
-- DROP TABLE currencymarket;
-- SELECT * FROM currencymarket;
-- easy
SELECT 
	userID, 
    userName, 
    dollarBalance, tomanBalance, lireBalance, poundBalance, euroBalance 
FROM wallet w, projschema.user u
WHERE u.userID = w.user_userID;

-- hard
SELECT 
	transactionID,
    u1.userName AS Seller,
    u2.userName AS Buyer,
    c1.name AS BaseCurrency,
    c2.name AS TargetCurrency
FROM 
	transaction t 
JOIN 
    user u1 ON t.user_sellerID = u1.userID
JOIN 
	user u2 ON t.user_buyerID1 = u2.userID
JOIN 
	currencyMarket c1 ON c1.currencyID = t.currency_fromID
JOIN
	currencyMarket c2 ON c2.currencyID = t.currency_toID
WHERE
	(t.date >'2009-01-01' AND t.date <'2010-01-01') AND 
    ((c1.name = 'toman' AND c2.name = 'dollar') OR (c1.name = 'dollar' AND c2.name = 'toman'));

-- harder 1
SELECT currency, monthNumber, buy, sell, buy+sell AS total FROM
(
 SELECT
    m.name AS currency,
    EXTRACT(MONTH FROM t.date) AS monthNumber,
    COALESCE(SUM(t2.amount), 0) AS buy,
    COALESCE(SUM(t3.amount2), 0) AS sell,
    COUNT(t2.amount) AS c1,
    COUNT(t3.amount2) AS c2
FROM
    currencyMarket m
JOIN
    transaction t ON m.currencyID = t.currency_fromID
LEFT JOIN
    (SELECT user_buyerID1, amount, currency_fromID FROM transaction WHERE EXTRACT(YEAR FROM date) = 2009) AS t2
    ON m.currencyID = t2.currency_fromID
LEFT JOIN
    (SELECT user_sellerID, amount2, currency_toID FROM transaction WHERE EXTRACT(YEAR FROM date) = 2009) AS t3
    ON m.currencyID = t3.currency_toID
WHERE
    EXTRACT(YEAR FROM t.date) = 2009
GROUP BY
    currency, monthNumber
    ) AS returned 
ORDER BY
    currency, monthNumber;



-- harder 2
SELECT
    userID,
    userName,
    a1 + a2 AS `total in dollars`
FROM
    (
        SELECT
            u.userID,
            u.userName,
            SUM(t1.amount) AS a1,
            SUM(t2.amount2) AS a2
        FROM
            user u
        JOIN
            (SELECT * FROM transaction WHERE currency_fromID = 0 AND currency_toID = 1) AS t1
            ON (u.userID = t1.user_buyerID1 OR u.userID = t1.user_sellerID)
        INNER JOIN
            (SELECT * FROM transaction WHERE currency_fromID = 1 AND currency_toID = 0) AS t2
            ON (u.userID = t2.user_buyerID1 OR u.userID = t2.user_sellerID)
        GROUP BY
            u.userID, u.userName
    ) AS returned
ORDER BY 
    `total in dollars` DESC
LIMIT 5;


-- harder 3
SELECT 
	sq1.curr1 AS 'currency 1', 
    sq1.curr2 AS 'currency 2', 
    count(t1.transactionID) AS 'number of transactions',
    SUM(amount) AS 'amount in dollors',
    FLOOR(SUM(amount) / NULLIF(count(t1.transactionID),0)) AS average
FROM ( SELECT transactionID, date, amount * cm1.buyRate / cm2.buyrate AS amount, currency_fromID, currency_toID 
	FROM transaction
    JOIN currencymarket cm1 ON currency_fromID = cm1.currencyID
    JOIN currencymarket cm2 ON cm2.currencyID = 0
		WHERE date>'2009-01-01' AND date<'2011-01-01' ) AS t1
JOIN
	(SELECT m1.currencyID AS currency1, m2.currencyID AS currency2, m1.name AS curr1, m2.name AS curr2
	FROM currencymarket m1 INNER JOIN currencymarket m2 ON m1.currencyID < m2.currencyID) AS sq1
ON ((sq1.currency1 = t1.currency_toID AND sq1.currency2 = t1.currency_fromID)OR (sq1.currency2 = t1.currency_toID AND sq1.currency1 = t1.currency_fromID)) 
 GROUP BY sq1.currency1, sq1.currency2;
