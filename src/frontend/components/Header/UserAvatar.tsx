import * as AvatarPrimitive from "@radix-ui/react-avatar"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

import { User } from "services/api.types"
import { getUserInitials } from "utils/user";

interface UserAvatarProps {
  user: User
}

type UserAvatarMergedProps = UserAvatarProps & React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Root>;

export default function UserAvatar({ user, ...props }: UserAvatarMergedProps) {
  return <Avatar {...props}>
    <AvatarImage title={user.name} src={user.image_url} aria-label={user.name} />
    <AvatarFallback>{getUserInitials(user)}</AvatarFallback>
  </Avatar>
}