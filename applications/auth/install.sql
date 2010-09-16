CREATE OR REPLACE VIEW adb2.users AS
SELECT userid, username, email, salt, password
FROM links.user u
WHERE u.userid IN (SELECT userid FROM adb2.allowed_users)
OR u.usergroupid IN (SELECT usergroupid FROM adb2.allowed_groups);