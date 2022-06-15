def trans_mhtml(filname):
    with open(filname, 'r+') as f:
        with open ('html_'+filname,'w+') as o:
            lines=f.readlines()
            for line in lines:
                if len(line)>=2:
                    line=line.replace('=3D','=')
                    o.write(line[:-2])
                    if line[-2]=='=':
                        pass
                    else:
                        o.write(line[-2:])
                else:
                    o.write(line)