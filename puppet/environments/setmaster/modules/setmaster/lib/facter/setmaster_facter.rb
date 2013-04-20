# collect facts from /etc/default/setmasterserver.conf if that file exists
# fail silently if it is not present so as not to break facter.
#
# /etc/default/setmasterserver.conf is a series of assignments:
# key1 value1
# ...
# keyn valuen
#
# lines prefixed a hash will be treated as comments and ignored
sm_key = nil
sm_value = nil
sm_args = {}

begin
    File.open("/etc/default/setmasterserver.conf").each do |line|
        sm_key = $1 and sm_value = $2 if line =~ /^\s*([\w,\-]+)[\s|\=]+([\w,\-,\/. :]+)/
        if sm_key != nil && sm_value != nil
            sm_args["sm_"+sm_key] = sm_value
            sm_key = nil
            sm_value = nil
            end
        end

    sm_args.each{|okey, oarg|
        Facter.add(okey) do
            setcode do
                oarg
            end
        end
    }
rescue
end
