#!/bin/bash
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


mountdir=/mnt/configdrive
filepath=$mountdir/cloudstack

user_data=$filepath/userdata/user-data.txt
availability_zone=$filepath/metadata/availability-zone.txt
cloud_identifier=$filepath/metadata/cloud-identifier.txt
instance_id=$filepath/metadata/instance-id.txt
local_hostname=$filepath/metadata/local-hostname.txt
service_offering=$filepath/metadata/service-offering.txt
vm_id=$filepath/metadata/vm-id.txt
public_key=$filepath/metadata/public-keys.txt
vm_password=$filepath/password/vm-password.txt

# If lable name is other than config, please change the below line as required
DefaultDisk=/dev/disk/by-label/config

function usage
{
    echo -e "USAGE: cloud-get-vm-data -options"
    echo -e "  where options include:"
    echo -e "\\t-m | --metadata [availability-zone | cloud-identifier | instance-id | local-hostname | service-offering | vm-id | public-key] \\n\\t\\tprint vm metadata"
    echo -e "\\t-p | --password \\n\\t\\tprint vm password"
    echo -e "\\t-u | --userdata \\n\\t\\tprint vm userdata"
}

function prepare_mount
{
    if [ ! -e $mountdir ]; then
        mkdir $mountdir
        chmod 700 $mountdir
    fi

    if [ -e $DefaultDisk ]; then
        Disk=$DefaultDisk
    else
        BLOCK_DEVICE=$(blkid -t LABEL='config-2' /dev/hd? /dev/sd? /dev/xvd? -o device)
        if [ -n $BLOCK_DEVICE ]; then
            Disk=$BLOCK_DEVICE
        else
            logger -t "cloud" "Unable to get the VM data: Config drive device not found"
            exit 1
        fi
    fi

    mount -r $Disk $mountdir
    if [ $? -ne 0 ]; then
        echo "Failed mounting $Disk to /mnt/configdrive"
        # exit 1  # be tolerant  # Kris
    fi
}

function remove_mount
{
  umount $mountdir
}

prepare_mount

case $1 in
    -u | --userdata )   echo -n "USERDATA: "
                        filename=$user_data
                        ;;
    -m | --metadata )   shift
                        if [ "$1" != "" ]; then
                            case $1 in
                                availability-zone ) echo -n "availability zone: ";  filename=$availability_zone
                                                    ;;
                                cloud-identifier )  echo -n "cloud identifier: ";   filename=$cloud_identifier
                                                    ;;
                                instance-id )       echo -n "instance-id: ";        filename=$instance_id
                                                    ;;
                                local-hostname )    echo -n "local-hostname: ";     filename=$local_hostname
                                                    ;;
                                service-offering )  echo -n "service-offering: ";   filename=$service_offering
                                                    ;;
                                vm-id )             echo -n  "vm-id: ";             filename=$vm_id
                                                    ;;
                                public-key )       echo -n  "public-key: ";         filename=$public_key
                                                    ;;
                                * )                 usage
                                                    remove_mount
                                                    exit 1
                            esac
                        else
                            echo -e "METADATA\\n"
                            [ -f $availability_zone ] && echo -e "availability zone:\t" "$(cat $availability_zone)"
                            [ -f $cloud_identifier ]  && echo -e "cloud identifier:\t"  "$(cat $cloud_identifier)"
                            [ -f $instance_id ]       && echo -e "instance-id:\t\t"     "$(cat $instance_id)"
                            [ -f $local_hostname ]    && echo -e "local-hostname:\t\t"  "$(cat $local_hostname)"
                            [ -f $service_offering ]  && echo -e "service-offering:\t"  "$(cat $service_offering)"
                            [ -f $vm_id ]             && echo -e "vm-id:\t\t\t"         "$(cat $vm_id)"
                            [ -f $public_key ]        && echo -e "public-key:\t\t"      "$(cat $public_key)"
                        fi
                        ;;
    -p | --password )   echo -n "PASSWORD: "
                        filename=$vm_password
                        ;;
    -h | --help )       usage
                        remove_mount
                        exit 0
                        ;;
    * )                 usage
                        remove_mount
                        exit 1
esac

if [ "$filename" != "" ] && [ -e $filename ]
then
    cat $filename
fi

exit 0
