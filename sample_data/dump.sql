create table if not exists "user"
(
	id serial not null
		constraint user_pkey
			primary key,
	first_name text not null,
	last_name text not null,
	email text not null,
	password text not null
)
;



create table if not exists question
(
	id serial not null
		constraint pk_question_id
			primary key,
	submission_time timestamp,
	view_number integer,
	vote_number integer,
	title text,
	message text,
	image text,
	user_id integer not null
		constraint question_user_id_fk
			references "user"
)
;



create table if not exists answer
(
	id serial not null
		constraint pk_answer_id
			primary key,
	submission_time timestamp,
	vote_number integer,
	question_id integer
		constraint fk_question_id
			references question,
	message text,
	image text,
	user_id integer not null
		constraint answer_user_id_fk
			references "user"
)
;


create table if not exists comment
(
	id serial not null
		constraint pk_comment_id
			primary key,
	question_id integer
		constraint fk_question_id
			references question,
	answer_id integer
		constraint fk_answer_id
			references answer,
	message text,
	submission_time timestamp,
	edited_count integer,
	user_id integer not null
		constraint comment_user_id_fk
			references "user"
)
;


