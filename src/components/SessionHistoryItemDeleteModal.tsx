import { type FC } from "react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface SessionHistoryItemDeleteModalProps {
  isOpen: boolean;
  onClose: () => void;
  onDelete: () => Promise<void>;
  isDeleting: boolean;
}

const SessionHistoryItemDeleteModal: FC<SessionHistoryItemDeleteModalProps> = ({
  isOpen,
  onClose,
  onDelete,
  isDeleting,
}) => (
  <Dialog open={isOpen} onOpenChange={onClose}>
    <DialogContent>
      <DialogHeader>
        <DialogTitle>Confirm delete session</DialogTitle>
        <DialogDescription>
          You are permanently deleting this session. This action is
          irreversible.
        </DialogDescription>
      </DialogHeader>
      <DialogFooter>
        <Button
          variant="outline"
          className=" border-border"
          onClick={onClose}
          disabled={isDeleting}
        >
          CANCEL
        </Button>
        <Button variant="destructive" onClick={onDelete} disabled={isDeleting}>
          DELETE
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
);

export default SessionHistoryItemDeleteModal;
