-- SQL Murder Mystery Challenge 
-- https://mystery.knightlab.com/


-- Information
--      Murder date: 2018-01-15
--      Murder location: SQL City


-- Database
-- crime_scene_report
--      date type description city            
-- drivers_license
--      id age height eye_color hair_color gender plate_number car_make car_model
-- facebook_event_checkin
--      person_id event_id event_name date
-- interview
--      person_id transcript
-- get_fit_now_member
--      id person_id name membership_start_date membership_status
-- get_fit_now_check_in
--      membership_id check_in_date check_in_time check_out_time
-- income
--      ssn annual_income
-- person
--      id name license_id address_number address_street_name ssn


-- Find the crime
SELECT 
    date,
    description
FROM
	crime_scene_report
WHERE
	`date` = "20180115"
	AND `city` = "SQL City"
	AND `type` = "murder"
; -- 1 record
-- Security footage shows that there were 2 witnesses.
-- The first witness lives at the last house on "Northwestern Dr".
-- The second witness, named Annabel, lives somewhere on "Franklin Ave".


-- Find witness 1 statement
SELECT
	person.name,
    interview.transcript
FROM
	person
    LEFT JOIN interview ON person.id = interview.person_id
WHERE
	person.address_street_name = "Northwestern Dr"
    AND person.address_number = (
        SELECT
            MAX(person.address_number)
        FROM
            person 
        WHERE
            person.address_street_name = "Northwestern Dr"
    )
; -- Morty Schapiro
-- I heard a gunshot and then saw a man run out.
-- He had a "Get Fit Now Gym" bag.
-- The membership number on the bag started with "48Z".
-- Only gold members have those bags.
-- The man got into a car with a plate that included "H42W".


-- Find witness 2 statement
SELECT
	person.name,
    interview.transcript
FROM
	person
    LEFT JOIN interview ON person.id = interview.person_id
WHERE
    person.name LIKE "Annabel%"
	AND person.address_street_name LIKE "Franklin%"
; -- Annabel Miller
-- I saw the murder happen, and I recognized the killer from my gym
-- when I was working out last week on January the 9th.


-- Find witness 1 POI
SELECT
	person.name,
    interview.transcript
FROM
	person 
	LEFT JOIN income USING (ssn)
	LEFT JOIN interview ON person.id = interview.person_id
	LEFT JOIN get_fit_now_member ON person.id = get_fit_now_member.person_id
	LEFT JOIN get_fit_now_check_in ON get_fit_now_member.id = get_fit_now_check_in.membership_id
	LEFT JOIN drivers_license ON person.license_id = drivers_license.id
WHERE
    get_fit_now_member.id LIKE "48Z%"
    AND get_fit_now_member.membership_status = "gold"
	AND drivers_license.plate_number LIKE "%H42W%"
; -- Jeremy Bowers


-- Find witness 2 POI
SELECT
	person.name,
	interview.transcript
FROM
	person 
	LEFT JOIN interview ON person.id = interview.person_id
	LEFT JOIN get_fit_now_member ON person.id = get_fit_now_member.person_id
	LEFT JOIN get_fit_now_check_in ON get_fit_now_member.id = get_fit_now_check_in.membership_id
WHERE
	get_fit_now_check_in.check_in_date = "20180109"
	AND interview.transcript IS NOT NULL
; -- Jeremy Bowers and others


-- Jeremy Bowers
-- I was hired by a woman with a lot of money.
-- I don't know her name but I know she's around 5'5" (65") or 5'7" (67").
-- She has red hair and she drives a Tesla Model S.
-- I know that she attended the SQL Symphony Concert 3 times in December 2017.


-- Follow statement from Jeremy Bowers
SELECT
	person.name,
	income.annual_income,
	drivers_license.car_make,
	drivers_license.car_model,
	facebook_event_checkin.event_name,
	facebook_event_checkin.date
FROM
	person
    LEFT JOIN income USING (ssn)
    LEFT JOIN facebook_event_checkin ON person.id = facebook_event_checkin.person_id
	LEFT JOIN drivers_license ON person.license_id = drivers_license.id
WHERE
	income.annual_income > 100000
    AND drivers_license.car_make = "Tesla"
	AND drivers_license.car_model = "Model S"
	AND drivers_license.gender = "female"
	AND drivers_license.hair_color = "red"
	AND drivers_license.height >= 65
	AND drivers_license.height <= 67
	AND facebook_event_checkin.event_name = "SQL Symphony Concert"
; -- Miranda Priestly


-- Complete person join
SELECT
	*
FROM
	person 
	LEFT JOIN income USING (ssn)
	LEFT JOIN interview ON person.id = interview.person_id
	LEFT JOIN facebook_event_checkin ON person.id = facebook_event_checkin.person_id
	LEFT JOIN get_fit_now_member ON person.id = get_fit_now_member.person_id
	LEFT JOIN get_fit_now_check_in ON get_fit_now_member.id = get_fit_now_check_in.membership_id
	LEFT JOIN drivers_license ON person.license_id = drivers_license.id
LIMIT
    1
;


-- Shortcut to answers!
SELECT person.name, interview.transcript FROM person LEFT JOIN interview ON person.id = interview.person_id WHERE LENGTH(interview.transcript) > 80;
