A:Dut-F# admin display-config
# TiMOS-B-0.0.I5189 both/x86_64 Nokia 7750 SR Copyright (c) 2000-2017 Nokia.
# All rights reserved. All use subject to applicable license agreements.
# Built on Mon May 29 18:06:07 PDT 2017 by builder in /rel0.0/I5189/panos/main

# Generated TUE SEP 11 21:18:07 2018 UTC

exit all
configure
#--------------------------------------------------
echo "System Configuration"
#--------------------------------------------------
    system
        name "Dut-F"
        boot-good-exec "ftp://andce2e02:tigris@andce2e02/./images/env.cfg"
        time
            ntp
                no shutdown
            exit
            sntp
                shutdown
            exit
            zone UTC
        exit
            bluetooth
            exit
    exit
#--------------------------------------------------
echo "System Security Configuration"
#--------------------------------------------------
    system
        security
            telnet-server
            ftp-server
            snmp
                community "uTdc9j48PBRkxn5DcSjchk" hash2 rwa version both
                community "Lla.RtAyRW2" hash2 r version both
            exit
            no per-peer-queuing
            cpu-protection
                link-specific-rate max
                policy 254 create
                exit
                policy 255 create
                exit
                port-overall-rate 15000
            exit
            dist-cpu-protection
                policy "_default-access-policy" create
                exit
                policy "_default-network-policy" create
                exit
            exit
        exit
    exit
#--------------------------------------------------
echo "System Login Control Configuration"
#--------------------------------------------------
    system
        login-control
            idle-timeout disable
            pre-login-message "andce2e02 - " name
        exit
    exit
#--------------------------------------------------
echo "Log Configuration"
#--------------------------------------------------
    log
        snmp-trap-group 90
            trap-target "138.203.221.173:162" address 138.203.221.173 snmpv2c notify-community "private"
        exit
        log-id 90
            from main change
            to snmp
            no shutdown
        exit
    exit
#--------------------------------------------------
echo "Card Configuration"
#--------------------------------------------------
    card 1
        card-type iom3-xp
        mda 1
            mda-type m60-10/100eth-tx
            no shutdown
        exit
        mda 2
            mda-type m60-10/100eth-tx
            no shutdown
        exit
        no shutdown
    exit
#--------------------------------------------------
echo "Port Configuration"
#--------------------------------------------------
    port 1/1/1
        ethernet
            mode access
        exit
        no shutdown
    exit
    port 1/1/2
        ethernet
            mtu 9212
        exit
        no shutdown
    exit
    port 1/1/3
        ethernet
            mode access
        exit
        no shutdown
    exit
    port 1/1/4
        ethernet
            mode access
        exit
        no shutdown
    exit
    port 1/1/5
        ethernet
        exit
        no shutdown
    exit
    port 1/1/6
        ethernet
        exit
        no shutdown
    exit
    port 1/1/7
        ethernet
        exit
        no shutdown
    exit
    port 1/1/8
        ethernet
        exit
        no shutdown
    exit
    port 1/1/9
        ethernet
        exit
        no shutdown
    exit
    port 1/1/10
        ethernet
        exit
        no shutdown
    exit
    port 1/1/11
        ethernet
        exit
        no shutdown
    exit
    port 1/1/12
        ethernet
        exit
        no shutdown
    exit
    port 1/1/13
        ethernet
        exit
        no shutdown
    exit
    port 1/1/14
        ethernet
        exit
        no shutdown
    exit
    port 1/1/15
        ethernet
        exit
        no shutdown
    exit
    port 1/1/16
        ethernet
        exit
        no shutdown
    exit
    port 1/1/17
        ethernet
        exit
        no shutdown
    exit
    port 1/1/18
        ethernet
        exit
        no shutdown
    exit
    port 1/1/19
        ethernet
        exit
        no shutdown
    exit
    port 1/1/20
        ethernet
        exit
        no shutdown
    exit
    port 1/1/21
        ethernet
        exit
        no shutdown
    exit
    port 1/1/22
        ethernet
        exit
        no shutdown
    exit
    port 1/1/23
        ethernet
        exit
        no shutdown
    exit
    port 1/1/24
        ethernet
        exit
        no shutdown
    exit
    port 1/1/25
        ethernet
        exit
        no shutdown
    exit
    port 1/1/26
        ethernet
        exit
        no shutdown
    exit
    port 1/1/27
        ethernet
        exit
        no shutdown
    exit
    port 1/1/28
        ethernet
        exit
        no shutdown
    exit
    port 1/1/29
        ethernet
        exit
        no shutdown
    exit
    port 1/1/30
        ethernet
        exit
        no shutdown
    exit
    port 1/1/31
        ethernet
        exit
        no shutdown
    exit
    port 1/1/32
        ethernet
        exit
        no shutdown
    exit
    port 1/1/33
        ethernet
        exit
        no shutdown
    exit
    port 1/1/34
        ethernet
        exit
        no shutdown
    exit
    port 1/1/35
        ethernet
        exit
        no shutdown
    exit
    port 1/1/36
        ethernet
        exit
        no shutdown
    exit
    port 1/1/37
        ethernet
        exit
        no shutdown
    exit
    port 1/1/38
        ethernet
        exit
        no shutdown
    exit
    port 1/1/39
        ethernet
        exit
        no shutdown
    exit
    port 1/1/40
        ethernet
        exit
        no shutdown
    exit
    port 1/1/41
        ethernet
        exit
        no shutdown
    exit
    port 1/1/42
        ethernet
        exit
        no shutdown
    exit
    port 1/1/43
        ethernet
        exit
        no shutdown
    exit
    port 1/1/44
        ethernet
        exit
        no shutdown
    exit
    port 1/1/45
        ethernet
        exit
        no shutdown
    exit
    port 1/1/46
        ethernet
        exit
        no shutdown
    exit
    port 1/1/47
        ethernet
        exit
        no shutdown
    exit
    port 1/1/48
        ethernet
        exit
        no shutdown
    exit
    port 1/1/49
        ethernet
        exit
        no shutdown
    exit
    port 1/1/50
        ethernet
        exit
        no shutdown
    exit
    port 1/1/51
        ethernet
        exit
        no shutdown
    exit
    port 1/1/52
        ethernet
        exit
        no shutdown
    exit
    port 1/1/53
        ethernet
        exit
        no shutdown
    exit
    port 1/1/54
        ethernet
        exit
        no shutdown
    exit
    port 1/1/55
        ethernet
        exit
        no shutdown
    exit
    port 1/1/56
        ethernet
        exit
        no shutdown
    exit
    port 1/1/57
        ethernet
        exit
        no shutdown
    exit
    port 1/1/58
        ethernet
        exit
        no shutdown
    exit
    port 1/1/59
        ethernet
        exit
        no shutdown
    exit
    port 1/1/60
        ethernet
        exit
        no shutdown
    exit
    port 1/2/1
        ethernet
        exit
        no shutdown
    exit
    port 1/2/2
        ethernet
        exit
        no shutdown
    exit
    port 1/2/3
        ethernet
        exit
        no shutdown
    exit
    port 1/2/4
        ethernet
        exit
        no shutdown
    exit
    port 1/2/5
        ethernet
        exit
        no shutdown
    exit
    port 1/2/6
        ethernet
        exit
        no shutdown
    exit
    port 1/2/7
        ethernet
        exit
        no shutdown
    exit
    port 1/2/8
        ethernet
        exit
        no shutdown
    exit
    port 1/2/9
        ethernet
        exit
        no shutdown
    exit
    port 1/2/10
        ethernet
        exit
        no shutdown
    exit
    port 1/2/11
        ethernet
        exit
        no shutdown
    exit
    port 1/2/12
        ethernet
        exit
        no shutdown
    exit
    port 1/2/13
        ethernet
        exit
        no shutdown
    exit
    port 1/2/14
        ethernet
        exit
        no shutdown
    exit
    port 1/2/15
        ethernet
        exit
        no shutdown
    exit
    port 1/2/16
        ethernet
        exit
        no shutdown
    exit
    port 1/2/17
        ethernet
        exit
        no shutdown
    exit
    port 1/2/18
        ethernet
        exit
        no shutdown
    exit
    port 1/2/19
        ethernet
        exit
        no shutdown
    exit
    port 1/2/20
        ethernet
        exit
        no shutdown
    exit
    port 1/2/21
        ethernet
        exit
        no shutdown
    exit
    port 1/2/22
        ethernet
        exit
        no shutdown
    exit
    port 1/2/23
        ethernet
        exit
        no shutdown
    exit
    port 1/2/24
        ethernet
        exit
        no shutdown
    exit
    port 1/2/25
        ethernet
        exit
        no shutdown
    exit
    port 1/2/26
        ethernet
        exit
        no shutdown
    exit
    port 1/2/27
        ethernet
        exit
        no shutdown
    exit
    port 1/2/28
        ethernet
        exit
        no shutdown
    exit
    port 1/2/29
        ethernet
        exit
        no shutdown
    exit
    port 1/2/30
        ethernet
        exit
        no shutdown
    exit
    port 1/2/31
        ethernet
        exit
        no shutdown
    exit
    port 1/2/32
        ethernet
        exit
        no shutdown
    exit
    port 1/2/33
        ethernet
        exit
        no shutdown
    exit
    port 1/2/34
        ethernet
        exit
        no shutdown
    exit
    port 1/2/35
        ethernet
        exit
        no shutdown
    exit
    port 1/2/36
        ethernet
        exit
        no shutdown
    exit
    port 1/2/37
        ethernet
        exit
        no shutdown
    exit
    port 1/2/38
        ethernet
        exit
        no shutdown
    exit
    port 1/2/39
        ethernet
        exit
        no shutdown
    exit
    port 1/2/40
        ethernet
        exit
        no shutdown
    exit
    port 1/2/41
        ethernet
        exit
        no shutdown
    exit
    port 1/2/42
        ethernet
        exit
        no shutdown
    exit
    port 1/2/43
        ethernet
        exit
        no shutdown
    exit
    port 1/2/44
        ethernet
        exit
        no shutdown
    exit
    port 1/2/45
        ethernet
        exit
        no shutdown
    exit
    port 1/2/46
        ethernet
        exit
        no shutdown
    exit
    port 1/2/47
        ethernet
        exit
        no shutdown
    exit
    port 1/2/48
        ethernet
        exit
        no shutdown
    exit
    port 1/2/49
        ethernet
        exit
        no shutdown
    exit
    port 1/2/50
        ethernet
        exit
        no shutdown
    exit
    port 1/2/51
        ethernet
        exit
        no shutdown
    exit
    port 1/2/52
        ethernet
        exit
        no shutdown
    exit
    port 1/2/53
        ethernet
        exit
        no shutdown
    exit
    port 1/2/54
        ethernet
        exit
        no shutdown
    exit
    port 1/2/55
        ethernet
        exit
        no shutdown
    exit
    port 1/2/56
        ethernet
        exit
        no shutdown
    exit
    port 1/2/57
        ethernet
        exit
        no shutdown
    exit
    port 1/2/58
        ethernet
        exit
        no shutdown
    exit
    port 1/2/59
        ethernet
        exit
        no shutdown
    exit
    port 1/2/60
        ethernet
        exit
        no shutdown
    exit
#--------------------------------------------------
echo "System Sync-If-Timing Configuration"
#--------------------------------------------------
    system
        sync-if-timing
            begin
            commit
        exit
    exit
#--------------------------------------------------
echo "Management Router Configuration"
#--------------------------------------------------
    router management
    exit

#--------------------------------------------------
echo "Router (Network Side) Configuration"
#--------------------------------------------------
    router Base
        interface "control"
            address 10.100.100.4/24
            port 1/1/2
            no shutdown
        exit
        interface "system"
            address 10.20.36.6/32
            no shutdown
        exit
        autonomous-system 1000
#--------------------------------------------------
echo "OSPFv2 Configuration"
#--------------------------------------------------
        ospf 0
            timers
                spf-wait 1000 spf-initial-wait 1000 spf-second-wait 1000
            exit
            area 0.0.0.0
                interface "control"
                    interface-type broadcast
                    hello-interval 5
                    dead-interval 15
                    no shutdown
                exit
            exit
            no shutdown
        exit
#--------------------------------------------------
echo "ISA Service Chaining Configuration"
#--------------------------------------------------
    exit

#--------------------------------------------------
echo "Service Configuration"
#--------------------------------------------------
    service
        customer 1 create
            description "Default customer"
        exit
        vprn 1111 customer 1 create
            interface "to-ce-vm" create
            exit
            interface "lo1" create
            exit
        exit
        vprn 1111 customer 1 create
            vrf-import "import"
            vrf-export "export"
            route-distinguisher 65534:36184
            auto-bind-tunnel
                resolution-filter
                    gre
                exit
                resolution filter
            exit
            interface "to-ce-vm" create
                address 192.168.1.1/24
                sap 1/1/1 create
                exit
            exit
            interface "lo1" create
                address 9.9.9.9/32
                loopback
            exit
            static-route-entry 0.0.0.0/0
                next-hop 192.168.1.2
                    no shutdown
                exit
            exit
            bgp
                import "import"
                export "export"
                rapid-withdrawal
                no shutdown
            exit
            no shutdown
        exit
    exit
#--------------------------------------------------
echo "Router (Service Side) Configuration"
#--------------------------------------------------
    router Base
#--------------------------------------------------
echo "OSPFv2 Configuration"
#--------------------------------------------------
        ospf 0
            no shutdown
        exit
#--------------------------------------------------
echo "Policy Configuration"
#--------------------------------------------------
        policy-options
            begin
            community "import" members "target:65534:36184"
            policy-statement "export"
                entry 10
                    action accept
                        community add "import"
                    exit
                exit
                default-action accept
                exit
            exit
            policy-statement "import"
                entry 10
                    from
                        community "import"
                    exit
                    action accept
                    exit
                exit
                default-action accept
                exit
            exit
            commit
        exit
#--------------------------------------------------
echo "BGP Configuration"
#--------------------------------------------------
        bgp
            family ipv4 vpn-ipv4 evpn
            connect-retry 5
            hold-time 120
            min-route-advertisement 1
            router-id 10.100.100.4
            rapid-withdrawal
            rapid-update evpn
            group "test"
                type internal
                neighbor 10.100.100.1
                    med-out 100
                    peer-as 1000
                exit
                neighbor 10.100.100.2
                    med-out 100
                    peer-as 1000
                exit
                neighbor 10.100.100.3
                    med-out 100
                    peer-as 1000
                exit
            exit
            no shutdown
        exit
    exit

#--------------------------------------------------
echo "System Time NTP Configuration"
#--------------------------------------------------
    system
        time
            ntp
                server 138.203.221.173
            exit
        exit
    exit

exit all

# Finished TUE SEP 11 21:18:10 2018 UTC


---

4EC public subnet in VSD :
RD : 65534:17510
RT : 65534:59238
