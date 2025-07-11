For the "Monitoring" VM, I modified "mysqld.cnf" file (specifically the line "bind-address") with 
the server IP (monitoring), I only allowed an especific IP (DEVCI) in the firewall and
I created an Mysql user on this VM with the client VM's IP (DEVCI) for added segurity.